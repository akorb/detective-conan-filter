from io import StringIO
import re

import pandas as pd
from common import get_html, to_ranges, sanitize_html

# flake8: noqa


def get_manga_count() -> int:
    volumes_html = get_html("https://conanwiki.org/wiki/Liste_der_Manga-B%C3%A4nde")
    volumes: list[str] = re.findall(r'Band \d+', volumes_html)
    return int(volumes[-1].split()[1])


def print_mangas(interests_pattern: str):
    manga_count = get_manga_count()

    # Manga 52 is the first manga with cases not part
    # of the german-synchronized anime.
    for manga_nr in range(52, manga_count + 1):
        url = f"https://conanwiki.org/wiki/Band_{manga_nr}"
        html = get_html(url)
        html = sanitize_html(html)

        df_list: list[pd.DataFrame] = \
            pd.read_html(StringIO(html),
                         attrs={'class': 'roundtable manga center'})
        assert len(df_list) == 1
        chapters_df = df_list[0]

        # Remove all chapters which contain no aspects of interest
        only_interests = chapters_df[chapters_df[('Legende', 'Legende')].str.contains(interests_pattern, regex=True, na=False)]

        relevant_volumes = only_interests[('Nummer', 'im Band')].to_list()
        if len(relevant_volumes) == 0:
            continue
        relevant_volumes = list(map(int, relevant_volumes))
        volumes_ranges = to_ranges(relevant_volumes)
        volumes_ranges = ['  ' + x for x in volumes_ranges]
        print('Manga:', manga_nr)
        print('\n'.join(volumes_ranges))

