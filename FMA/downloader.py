import subprocess
import time
import csv
import os

def open_firefox() -> subprocess.Popen:
    """Open Firefox."""
    try:
        print("Opening Firefox...")
        firefox_process = subprocess.Popen(["firefox"])
        print("Waiting 5 seconds for Firefox to fully launch...")
        time.sleep(5)  # Allow enough time for Firefox to start
        return firefox_process
    except Exception as e:
        print(f"Failed to open Firefox: {e}")
        return None

def open_new_tab_and_navigate(track_url: str) -> None:
    """Open a new tab in Firefox and navigate to the specified track URL."""
    try:
        # Open a new tab using keyboard shortcut (Ctrl+T)
        subprocess.run(["xdotool", "key", "ctrl+t"], check=True)
        time.sleep(0.5)  # Short wait for the new tab to open

        # Type the URL and press Enter
        subprocess.run(["xdotool", "type", track_url], check=True)
        subprocess.run(["xdotool", "key", "Return"], check=True)

        time.sleep(1)  # Brief delay to allow the URL to start loading
        # Close the current tab (Ctrl+W)
        subprocess.run(["xdotool", "key", "ctrl+w"], check=True)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while opening a new tab: {e}")

def trigger_download_from_csv(csv_file: str, batch_size: int = 10) -> None:
    """Read the CSV file and open each song's download link in Firefox in batches."""
    download_folder = os.path.dirname(os.path.abspath(csv_file))  # Directory where CSV is located

    # Open Firefox
    firefox_process = open_firefox()
    
    if not firefox_process:
        print("Failed to open Firefox. Exiting.")
        return

    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header

        batch_urls = []

        for row in reader:
            song_name, download_link = row
            batch_urls.append(download_link)

            # If batch is full, open all tabs and then reset the batch
            if len(batch_urls) == batch_size:
                # Open each URL in a new tab
                for url in batch_urls:
                    open_new_tab_and_navigate(url)
                    time.sleep(1)  # Small delay between opening tabs

                # Allow time for all tabs to load
                time.sleep(10)  # Increase based on how long it takes to load the pages

                # Close all opened tabs except the first one
                for _ in batch_urls:
                    subprocess.run(["xdotool", "key", "ctrl+w"], check=True)
                    time.sleep(1)  # Small delay to ensure tab closes properly

                # Reset batch
                batch_urls = []

        # Process any remaining URLs that didn't fill the last batch
        if batch_urls:
            for url in batch_urls:
                open_new_tab_and_navigate(url)
                time.sleep(1)  # Small delay between opening tabs

            # Allow time for all tabs to load
            time.sleep(20)

            # Close all remaining tabs
            for _ in batch_urls:
                subprocess.run(["xdotool", "key", "ctrl+w"], check=True)
                time.sleep(1)

    # Optionally, close Firefox after the downloads are done
    firefox_process.terminate()


if __name__ == "__main__":
    # Example of triggering the download manually
    csv_file = "path/to/your/csv_file.csv"
    trigger_download_from_csv(csv_file)
