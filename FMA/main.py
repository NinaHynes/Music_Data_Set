from fetch import fetch_page_content, fetch_and_print_genre_pages
from parse import extract_genres
from display import display_genres
from folders import create_folders
from colorama import Fore, Style  # Import Fore and Style
from typing import Dict
import re



def main(url: str) -> None:
    default_page_size = 20
    html_content = fetch_page_content(url, default_page_size)
    genres = extract_genres(html_content)

    exclude_list = [
        "Sign in", "Sign up", "Blog", "About", "Donate", "Contact us",
        "Helpdesk", "Search", "List of artists", "Web monetized", "Royalty free music", "Featured mixes", "Top downloads", "Browse by genre", "About Tribe of Noise", "About FMA", "Helping musicians", "Discover", "Log in", "Create"
    ]

    display_genres(genres, exclude=exclude_list)
    allowed_genres = [(name, url) for name, url in genres if name not in exclude_list]

    folder_song_counts = {}
    create_folders(allowed_genres, folder_song_counts)

    fetch_and_print_genre_pages(allowed_genres, folder_song_counts)

if __name__ == "__main__":
    page_url = 'https://freemusicarchive.org/genres'
    main(page_url)



#https://github.com/mozilla/geckodriver/releases
