from io import StringIO

import pandas as pd
from common import get_html, to_ranges, sanitize_html

# flake8: noqa


def print_animes(interests_pattern: str):
    html = get_html("https://conanwiki.org/wiki/Liste_der_Anime-Episoden")
    html = sanitize_html(html)

    all_seasons: list[pd.DataFrame] = pd.read_html(StringIO(html),
                                                   converters={0: str},
                                                   attrs={'class': 'roundtable anime center'})
    # seasons synced in german have 8 columns
    # later japanese-only seasons have 7 columns since the german release date is missing
    german_seasons = filter(lambda table: len(table.columns) == 8, all_seasons)

    dfs = []
    for season in german_seasons:
        season.drop(['Bild', 'Deutscher Titel', 'Übersetzter Titel', 'Erstausstrahlung', 'Originaltitel Titel in Rōmaji'],
                    axis=1,
                    level=0,
                    errors='ignore',
                    inplace=True)

        # We need to rename the second level of the first column that it stays consistent
        # over all tables such that we can concat them nicely later
        season.rename(columns={season.columns[0][1]: 'Anime'}, inplace=True, level=1)

        # Remove fillers
        no_fillers = season[~season[('Nummer', 'Manga (Fall)')].str.contains("Filler")]

        # Remove all episodes which contain no aspects of interest
        only_interests = no_fillers[no_fillers[('Geschichte', 'Geschichte')].str.contains(interests_pattern, regex=True, na=False)]
        dfs.append(only_interests)

    episodes_filtered = pd.concat(dfs)

    # Use the german episode numbers. Remove the japanese ones.
    episodes_filtered[('Nummer', 'Anime')] = episodes_filtered[('Nummer', 'Anime')].apply(lambda x: x.split(' ')[0])

    episodes_list = episodes_filtered[('Nummer', 'Anime')].to_list()
    episodes_list = list(map(int, episodes_list))
    episodes_ranges = to_ranges(episodes_list)
    print('\n'.join(episodes_ranges))
