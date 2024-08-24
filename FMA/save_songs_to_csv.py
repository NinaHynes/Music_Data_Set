import csv
import os
from typing import List, Tuple

def save_songs_to_csv(genre: str, song_data: List[Tuple[str, str]], folder_path: str) -> None:
    """
    Save the song names and download links to a CSV file in the corresponding genre folder.
    
    Args:
        genre (str): The genre name.
        song_data (List[Tuple[str, str]]): List of tuples where each tuple contains a song name and its download link.
        folder_path (str): The path to the genre folder where the CSV file will be saved.
    """
    csv_filename = f"FMA_{genre}.csv"
    csv_filepath = os.path.join(folder_path, csv_filename)
    
    with open(csv_filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Song Name", "Download Link"])  # Header row
        for song_name, download_link in song_data:
            writer.writerow([song_name, download_link])
    
    print(f"CSV file saved: {csv_filepath}")


def read_songs_from_csv(genre: str, folder_path: str) -> List[Tuple[str, str]]:
    """
    Read the song names and download links from a CSV file in the corresponding genre folder.
    
    Args:
        genre (str): The genre name.
        folder_path (str): The path to the genre folder where the CSV file is saved.
    
    Returns:
        List[Tuple[str, str]]: A list of tuples where each tuple contains a song name and its download link.
    """
    csv_filename = f"FMA_{genre}.csv"
    csv_filepath = os.path.join(folder_path, csv_filename)

    if not os.path.exists(csv_filepath):
        print(f"CSV file not found: {csv_filepath}")
        return []

    song_data = []
    with open(csv_filepath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) == 2:
                song_data.append((row[0], row[1]))

    print(f"Read {len(song_data)} songs from CSV file: {csv_filepath}")
    return song_data