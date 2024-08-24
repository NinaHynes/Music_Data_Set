import subprocess
import time
import csv
import requests
from bs4 import BeautifulSoup
import shutil
import os

def create_custom_firefox_profile(profile_dir: str, download_dir: str) -> None:
    """Create a Firefox profile directory and add user.js configuration."""
    os.makedirs(profile_dir, exist_ok=True)
    
    # Define the content for user.js
    user_js_content = """
    user_pref("browser.download.folderList", 2);
    user_pref("browser.download.dir", "{download_dir}");
    user_pref("browser.helperApps.neverAsk.saveToDisk", "audio/mpeg,application/octet-stream");
    """.format(download_dir=os.path.abspath(download_dir))

    # Write the content to user.js
    with open(os.path.join(profile_dir, "user.js"), 'w') as f:
        f.write(user_js_content)
    
    print(f"Custom profile created at: {profile_dir}")


def handle_download_song(download_url: str, profile_dir: str) -> None:
    """Trigger the download of the song from the given URL using the custom Firefox profile."""
    try:
        # Open Firefox with the custom profile to ensure it uses the correct settings
        firefox_process = open_firefox(profile_dir)
        if firefox_process:
            open_new_tab_and_navigate(download_url)
            # Optionally, close Firefox after the download
            firefox_process.terminate()
    except Exception as e:
        print(f"Failed to handle download: {e}")


def open_firefox(profile_dir: str) -> subprocess.Popen:
    """Open Firefox with a specified profile directory."""
    try:
        print("Opening Firefox with custom profile...")
        firefox_process = subprocess.Popen(["firefox", "-profile", profile_dir])
        print("Waiting 5 seconds for Firefox to fully launch...")
        time.sleep(5)
        return firefox_process
    except Exception as e:
        print(f"Failed to open Firefox: {e}")
        return None

def open_new_tab_and_navigate(track_url: str) -> None:
    """Open a new tab in Firefox, navigate to the specified track URL, and close the tab."""
    try:
        # Open a new tab using keyboard shortcut (Ctrl+T)
        subprocess.run(["xdotool", "key", "ctrl+t"], check=True)
        time.sleep(1)  # Wait for the new tab to open

        # Type the URL and press Enter
        subprocess.run(["xdotool", "type", track_url], check=True)
        subprocess.run(["xdotool", "key", "Return"], check=True)

        # Wait for the page to load and perform actions (adjust time as necessary)
        time.sleep(2)  # Adjust this delay based on how long it takes to load the page

        # Close the current tab (Ctrl+W)
        subprocess.run(["xdotool", "key", "ctrl+w"], check=True)
        time.sleep(1)  # Wait a bit before opening a new tab

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while managing tabs: {e}")

def trigger_download_from_csv(csv_file: str, download_folder) -> None:
    """Read the CSV file and open each song's download link in Firefox."""
    download_folder = os.path.dirname(os.path.abspath(csv_file))  # Directory where CSV is located
    profile_dir = os.path.join(download_folder, "firefox_profile")

    # Create Firefox profile with custom settings
    create_custom_firefox_profile(profile_dir, download_folder)

    # Open Firefox
    firefox_process = open_firefox(profile_dir)
    
    if not firefox_process:
        print("Failed to open Firefox. Exiting.")
        return

    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header

        for row in reader:
            song_name, download_link = row
            output_file = os.path.join(download_folder, f"{song_name}.mp3")
            
            # Open new tab, navigate to the URL, and close the tab
            open_new_tab_and_navigate(download_link)

            # Handle the downloaded song
            handle_download_song(download_link, output_file, download_folder)
    
    # Optionally, close Firefox after the downloads are done
    firefox_process.terminate()


if __name__ == "__main__":
    # Example of triggering the download manually
    csv_file = "path/to/your/csv_file.csv"
    download_folder = "path/to/your/download/folder"
    trigger_download_from_csv(csv_file, download_folder)
