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
