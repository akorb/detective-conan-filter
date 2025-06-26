import argparse
import re
import sys

import requests

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


def get_interests_regex_from_args() -> tuple[str, str]:
    parser = argparse.ArgumentParser(description='See https://conanwiki.org/wiki/ConanWiki:Legende_(Geschichte) for a more thorough explanation of the episode types.')
    parser.add_argument('media_type', choices=["manga", "anime"], help="Must be either 'manga' or 'anime'.")
    parser.add_argument('--new-character', action='store_const', const=Charakter, help=Charakter)
    parser.add_argument('--relationship', action='store_const', const=Beziehung, help=Beziehung)
    parser.add_argument('--detective-boys', action='store_const', const=DB, help=DB)
    parser.add_argument('--parents', action='store_const', const=Eltern, help=Eltern)
    parser.add_argument('--antidote', action='store_const', const=Gegengift, help=Gegengift)
    parser.add_argument('--new-item', action='store_const', const=Gegenstand, help=Gegenstand)
    parser.add_argument('--fbi-cia', action='store_const', const=Geheim_FBI_CIA, help=Geheim_FBI_CIA)
    parser.add_argument('--heiji', action='store_const', const=Heiji, help=Heiji)
    parser.add_argument('--kaito-kid', action='store_const', const=Kaito_Kid, help=Kaito_Kid)
    parser.add_argument('--men-in-black', action='store_const', const=Organisation, help=Organisation)
    parser.add_argument('--past', action='store_const', const=Vergangenheit, help=Vergangenheit)
    parser.add_argument('--important', action='store_const', const=Wichtig, help=Wichtig)

    parsed = parser.parse_args(sys.argv[1:])
    args_dic = vars(parsed)
    media_type = args_dic.pop('media_type')

    interests_pattern = "|".join(filter(None, args_dic.values()))

    if not interests_pattern:
        print("You must select at least one interest.")
        parser.print_usage()
        sys.exit(0)

    return media_type, interests_pattern

def get_html(url: str) -> str:
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Request failed with response code {response.status_code}")
        sys.exit(1)

    return response.text


def sanitize_html(html: str) -> str:
    # pandas only uses the inner text of each cell on the html table.
    # but the "Geschichte" column does not have any text, only images.
    # This regex converts replaces <img alt="asdf" ...> to "asdf",
    # i.e., to plain text.
    new_html = re.sub(r'<img alt="(.*?)" .*? />', r'\1', html)
    return new_html


def to_ranges(numbers: list[int]) -> list[str]:
    if len(numbers) == 0:
        return []

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
