from bs4 import BeautifulSoup
import requests
import re
from colorama import Fore, Style  # Import Fore and Style
from typing import Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from save_songs_to_csv import save_songs_to_csv
import os
from downloader import trigger_download_from_csv



def fetch_page_content(url: str, page_size: int) -> str:
    """Fetch the HTML content of a given URL with a specific page size."""
    full_url = f"{url}?pageSize={page_size}&page=1&search-genre=Jazz&sort=date&d=0"
    response = requests.get(full_url)
    response.raise_for_status()
    return response.text



def fetch_and_print_genre_pages(allowed_genres, folder_song_counts):
    """Fetch and print the content for each genre page, and extract URLs from data-url attributes."""
    genre_dict = {name: url for name, url in allowed_genres}

    with ThreadPoolExecutor() as executor:
        future_to_genre = {}

        for genre in folder_song_counts.keys():
            genre_url = genre_dict.get(genre)
            if genre_url:
                print(f"Fetching content for genre: {genre}")
                try:
                    max_songs = folder_song_counts[genre]
                    page_size = 100

                    # Submit a new task to the executor
                    future = executor.submit(fetch_all_pages, genre_url, page_size, max_songs, genre)
                    future_to_genre[future] = genre

                except Exception as e:
                    print(f"Failed to submit task for genre {genre}. Error: {e}")

        # Collect results as they complete
        for future in as_completed(future_to_genre):
            genre = future_to_genre[future]
            try:
                html_content = future.result()
                soup = BeautifulSoup(html_content, 'html.parser')
                song_data = []  # Move song_data initialization here

                for a_tag in soup.find_all('a', href=True):
                    data_url = a_tag.get('data-url')
                    if data_url and re.match(r'^https://freemusicarchive.org/track/.*(downloadOverlay|download)/$', data_url):
                        # Convert the link to a download link
                        download_link = re.sub(r'downloadOverlay', 'download', data_url)
                        # Extract the song name from the URL
                        song_name_match = re.search(r'/track/([^/]+)/download/', download_link)
                        if song_name_match:
                            song_name = song_name_match.group(1)
                            song_data.append((song_name, download_link))

                            # Print song information
                            print(f"Song Name: {song_name}")
                            print(f"{genre} converted link: {download_link}\n")

                # After processing all songs for this genre, save them to a CSV
                if song_data:
                    # Determine the folder path for this genre
                    folder_path = os.path.join(os.getcwd(), genre)
                    os.makedirs(folder_path, exist_ok=True)  # Ensure folder exists
                    # Save the song data to a CSV file in the genre folder
                    save_songs_to_csv(genre, song_data, folder_path)
                    # Trigger download after saving CSV
                    csv_file_path = os.path.join(folder_path, f"FMA_{genre}.csv")
                    trigger_download_from_csv(csv_file_path, folder_path)

            except Exception as e:
                print(f"Error fetching data for genre '{genre}': {e}")

    print(Fore.GREEN + Style.BRIGHT + "All tasks completed." + Style.RESET_ALL)


def fetch_all_pages(base_url: str, page_size: int, max_songs: int, genre: str) -> str:
    """Fetch HTML content from multiple pages until the required number of songs is reached.
    
    Args:
        base_url (str): The base URL of the genre page.
        page_size (int): Number of items per page (typically 100).
        max_songs (int): Maximum number of songs to fetch.
        genre (str): The genre to be used in the URL.
    
    Returns:
        str: Combined HTML content from all pages.
    """
    all_track_links = []
    all_content = ""
    page_number = 1
    total_songs_fetched = 0
    
    # Calculate the total number of pages needed
    total_pages = (max_songs ) // page_size
    # Debug: Start fetching process
    print(f"Starting to fetch songs for max_songs={max_songs} with page_size={page_size}...")
    print(f"Total pages to fetch: {total_pages}")
  

    # Debug: Start fetching process
    print(f"Starting to fetch songs for max_songs={max_songs} with page_size={page_size}...")

    while page_number <= total_pages and total_songs_fetched < max_songs :
        # Calculate the remaining number of songs to fetch
        remaining_songs = max_songs - total_songs_fetched
        current_page_size = min(page_size, remaining_songs)

         # Construct URL for the current page with adjusted page size and dynamic genre
        url = f"{base_url}?pageSize={current_page_size}&page={page_number}&search-genre={genre}&sort=date&d=0"

        # Debug: Print URL and page info
        print(f"Fetching page {page_number} with page size {current_page_size}. URL: {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()  # Ensure we notice bad responses
        except requests.RequestException as e:
            print(f"Error fetching page {page_number}: {e}")
            break

        
        page_content = response.text
        all_content += page_content

        # Parse the HTML content
        soup = BeautifulSoup(page_content, 'html.parser')
        track_links = [a['href'] for a in soup.find_all('a', href=True) if 'downloadOverlay' in a['href']]
        num_links_on_page = len(track_links)
        print(f"Links found on page {page_number}: {num_links_on_page}")

        # Update total songs fetched
        total_songs_fetched += num_links_on_page
        all_track_links.extend(track_links)

         # Debug: Print the cumulative number of songs fetched so far
        print(f"Total songs fetched so far: {total_songs_fetched}")

        # Stop fetching if no more songs are found
        
        page_number += 1

        # If we reach or exceed the max_songs, stop fetching
        if total_songs_fetched >= max_songs:
            print(f"Reached or exceeded the target of {max_songs} songs. Stopping.")
            break
        
       # Debug: Print the total songs fetched at the end
    print(f"Finished fetching. Total songs fetched: {total_songs_fetched}")

    return all_content
