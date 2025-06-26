import pandas as pd
import requests
import sys
from io import StringIO
import re

# flake8: noqa

Beziehung = "Beziehung zweier oder mehrerer Haupt- oder Nebencharaktere"
Charakter = "Neue Haupt- oder Nebencharaktere"
DB = "Auftritt der Detective Boys"
Eltern = "Auftritt von Eri Kisaki, Yusaku oder Yukiko Kudo"
Gegengift = "Conan Edogawa oder Ai Haibara nimmt ein Gegengift für das Apoptoxin 4869 ein"
Gegenstand = "Ein neuer Gegenstand wird eingeführt, der im Laufe der Serie öfter benutzt wird"
Geheim_FBI_CIA = "Auftritt des FBIs, der CIA oder einzelner Mitglieder"
Heiji = "Auftritt von Heiji Hattori"
Kaito_Kid = "Auftritt von Kaito Kid"
Organisation = "Auftritt der Organisation oder einzelner Mitglieder"
Vergangenheit = "Vergangenheit einzelner oder mehrerer Haupt- oder Nebencharaktere"
Wichtig = "Wichtige Handlungen für den Verlauf der Serie"

# Specify here in which kinds of episodes you're interested
interests = [Beziehung, Charakter, Eltern, Gegengift, Gegenstand, Geheim_FBI_CIA, Heiji,
             Kaito_Kid, Organisation, Vergangenheit, Wichtig]


def get_html():
    url = "https://conanwiki.org/wiki/Liste_der_Anime-Episoden"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Request failed with response code {response.status_code}")
        sys.exit(1)

    return response.text


def to_ranges(numbers: list[int]) -> list[str]:
    results = []
    start = numbers[0]
    end = start

    for n in numbers[1:]:
        if n == end + 1:
            end = n
        else:
            if start == end:
                results.append(str(start))
            else:
                results.append(f"{start} – {end}")
            start = n
            end = n

    # Append the last range/group
    if start == end:
        results.append(str(start))
    else:
        results.append(f"{start} – {end}")

    return results


def main():
    html = get_html()

    # pandas only uses the inner text of each cell on the html table.
    # but the "Geschichte" column does not have any text, only images.
    # This regex converts replaces <img alt="asdf" ...> to "asdf",
    # i.e., to plain text.
    html = re.sub(r'<img alt="(.*?)" .*? />', r'\1', html)

    interests_pattern = "|".join(interests)

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


if __name__ == "__main__":
    main()
