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

def get_html(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Request failed with response code {response.status_code}")
        sys.exit(1)

    return response.text


def get_manga_count() -> int:
    url = "https://conanwiki.org/wiki/Liste_der_Manga-B%C3%A4nde"
    response = requests.get(url)

    text = response.text
    volumes: list[str] = re.findall(r'Band \d+', text)
    return int(volumes[-1].split()[1])


def main():
    interests_pattern = "|".join(interests)

    manga_count = get_manga_count()

    for manga_nr in range(52, manga_count + 1):
        url = f"https://conanwiki.org/wiki/Band_{manga_nr}"
        html = get_html(url)

        # pandas only uses the inner text of each cell on the html table.
        # but the "Geschichte" column does not have any text, only images.
        # This regex converts replaces <img alt="asdf" ...> to "asdf",
        # i.e., to plain text.
        html = re.sub(r'<img alt="(.*?)" .*? />', r'\1', html)

        df_list: list[pd.DataFrame] = \
            pd.read_html(StringIO(html),
                         attrs={'class': 'roundtable manga center'})
        assert(len(df_list) == 1)
        chapters_df = df_list[0]

        # Remove all chapters which contain no aspects of interest
        only_interests = chapters_df[chapters_df[('Legende', 'Legende')].str.contains(interests_pattern, regex=True, na=False)]

        relevant_volumes = only_interests[('Nummer', 'im Band')].to_list()
        relevant_volumes = list(map(int, relevant_volumes))
        volumes_ranges = to_ranges(relevant_volumes)
        volumes_ranges = ['  ' + x for x in volumes_ranges]
        print('Manga:', manga_nr)
        print('\n'.join(volumes_ranges))


if __name__ == "__main__":
    main()
