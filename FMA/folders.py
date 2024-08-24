import os
from typing import List, Dict, Tuple
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

def create_folders(allowed_genres: List[Tuple[str, str]], folder_song_counts: Dict[str, int]) -> None:
    """Prompt the user to create folders with specified names."""
    genre_dict = {genre_name.lower(): (genre_name, genre_url) for genre_name, genre_url in allowed_genres}
    
    while True:
        folder_name_input = input(Fore.YELLOW + "Enter the name of the folder you want to create (or type 'done' to finish): " + Style.RESET_ALL)
        folder_name_input = folder_name_input.strip()

        if folder_name_input.lower() == 'done':
            break
        
        folder_name_key = folder_name_input.lower()
        if folder_name_key in genre_dict:
            genre_name, genre_url = genre_dict[folder_name_key]
            folder_path = os.path.join(os.getcwd(), genre_name)
            os.makedirs(folder_path, exist_ok=True)
            print(Fore.GREEN + f"Created folder: {folder_path}" + Style.RESET_ALL)

            while True:
                num_songs_input = input(Fore.YELLOW + f"How many songs do you want in the '{genre_name}' folder? " + Style.RESET_ALL)
                try:
                    num_songs = int(num_songs_input)
                    if num_songs < 20:
                        print(Fore.RED + "Error: You must request at least 20 songs." + Style.RESET_ALL)
                        num_songs = 20
                    folder_song_counts[genre_name] = num_songs
                    break
                except ValueError:
                    print(Fore.RED + "Error: Please enter a valid number." + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Error: '{folder_name_input}' is not a valid genre. Please choose from the available genres." + Style.RESET_ALL)

    print(Fore.GREEN + "Folder and song counts:" + Style.RESET_ALL)
    for genre, count in folder_song_counts.items():
        print(f"- {Fore.CYAN}{genre}: {count} songs{Style.RESET_ALL}")
