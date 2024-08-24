from typing import List, Tuple
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

def display_genres(genres: List[Tuple[str, str]], exclude: List[str] = None) -> None:
    """Display the genres and their URLs with colored output."""
    if exclude is None:
        exclude = []

    filtered_genres = [genre for genre in genres if genre[0] not in exclude]

    print(Fore.GREEN + Style.BRIGHT + "Available Music Genres:" + Style.RESET_ALL)
    for genre_name, genre_url in filtered_genres:
        print(f"- {Fore.CYAN}{genre_name}{Style.RESET_ALL} ({genre_url})")

    print(Fore.YELLOW + Style.BRIGHT + "\nFeel free to choose one of these genres to collect its music!" + Style.RESET_ALL)
