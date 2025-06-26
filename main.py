from common import get_interests_regex_from_args
from anime import print_animes
from mangas import print_mangas


def main():
    media_type, interests_pattern = get_interests_regex_from_args()
    if media_type == 'anime':
        print_animes(interests_pattern)
    elif media_type == 'manga':
        print_mangas(interests_pattern)
    else:
        print("Should never happen")


if __name__ == "__main__":
    main()
