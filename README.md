## Usage

```
usage: main.py [-h] [--new-character] [--relationship] [--detective-boys] [--parents] [--antidote] [--new-item] [--fbi-cia] [--heiji] [--kaito-kid] [--men-in-black]
               [--past] [--important]
               {manga,anime}

See https://conanwiki.org/wiki/ConanWiki:Legende_(Geschichte) for a more thorough explanation of the episode types.

positional arguments:
  {manga,anime}     Must be either 'manga' or 'anime'.

options:
  -h, --help        show this help message and exit
  --new-character   Neue Haupt- oder Nebencharaktere
  --relationship    Beziehung zweier oder mehrerer Haupt- oder Nebencharaktere
  --detective-boys  Auftritt der Detective Boys
  --parents         Auftritt von Eri Kisaki, Yusaku oder Yukiko Kudo
  --antidote        Conan Edogawa oder Ai Haibara nimmt ein Gegengift für das Apoptoxin 4869 ein
  --new-item        Ein neuer Gegenstand wird eingeführt, der im Laufe der Serie öfter benutzt wird
  --fbi-cia         Auftritt des FBIs, der CIA oder einzelner Mitglieder
  --heiji           Auftritt von Heiji Hattori
  --kaito-kid       Auftritt von Kaito Kid
  --men-in-black    Auftritt der Organisation oder einzelner Mitglieder
  --past            Vergangenheit einzelner oder mehrerer Haupt- oder Nebencharaktere
  --important       Wichtige Handlungen für den Verlauf der Serie
```

## Setup environment, e.g. install dependencies

```sh
uv sync
```

## Get episodes/chapters of interest

```sh
uv run main.py anime --new-character ...
# or
uv run main.py manga --new-character ...
```
