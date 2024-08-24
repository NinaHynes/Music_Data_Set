# import requests

# def login_and_download(url, login_url, email, password, download_url, output_file):
#     # Start a session
#     session = requests.Session()
    
#     # Step 1: Get the login page to retrieve the CSRF token
#     login_page = session.get(login_url)
#     login_page.raise_for_status()
    
#     # Extract CSRF token from the login page
#     from bs4 import BeautifulSoup
#     soup = BeautifulSoup(login_page.text, 'html.parser')
#     csrf_token = soup.find('input', {'name': '_token'}).get('value')

#     # Step 2: Prepare the login data
#     login_data = {
#         'email': email,
#         'password': password,
#         '_token': csrf_token,
#         'remember': 'on'  # If you want to stay logged in
#     }
    
#     # Step 3: Send the POST request to log in
#     response = session.post(login_url, data=login_data)
#     response.raise_for_status()
    
#     # Check if login was successful by looking for a specific element or redirect
#     if "Sign in to an existing account" in response.text:
#         print("Login failed! Check your credentials.")
#         return
    
#     print("Login successful!")

#     # Step 4: Download the MP3 file
#     download_response = session.get(download_url)
#     download_response.raise_for_status()

#     # Step 5: Save the MP3 file
#     with open(output_file, 'wb') as file:
#         file.write(download_response.content)
    
#     print(f"MP3 file downloaded successfully and saved as {output_file}!")

# if __name__ == "__main__":
#     # Define the URLs and credentials
#     url = "https://freemusicarchive.org/track/horse-market-share-instrumental/download/"
#     login_url = "https://freemusicarchive.org/login"
#     email = "abdoelnamaki@gmail.com"
#     password = "-~^r@}Vx5Qs7=kX"
#     output_file = "horse_market_share_instrumental.mp3"

#     # Call the function
#     login_and_download(url, login_url, email, password, url, output_file)
import csv
import os
import requests
from bs4 import BeautifulSoup

def download_song(session, download_url, output_file):
    """Download a single song using the provided session."""
    try:
        download_response = session.get(download_url)
        download_response.raise_for_status()
        with open(output_file, 'wb') as file:
            file.write(download_response.content)
        print(f"MP3 file downloaded successfully and saved as {output_file}!")
    except Exception as e:
        print(f"Failed to download {output_file}. Error: {e}")

def login_and_create_session(login_url, email, password):
    """Log in and return a session with cookies."""
    session = requests.Session()
    login_page = session.get(login_url)
    login_page.raise_for_status()

    soup = BeautifulSoup(login_page.text, 'html.parser')
    csrf_token = soup.find('input', {'name': '_token'}).get('value')

    login_data = {
        'email': email,
        'password': password,
        '_token': csrf_token,
        'remember': 'on'
    }

    response = session.post(login_url, data=login_data)
    response.raise_for_status()

    if "Sign in to an existing account" in response.text:
        print("Login failed! Check your credentials.")
        return 
    
    print("Login successful!")
    return session

def trigger_download_from_csv(csv_file, download_folder):
    """Read the CSV and download each song sequentially."""
    login_url = "https://freemusicarchive.org/login"
    email = "abdoelnamaki@gmail.com"
    password = "-~^r@}Vx5Qs7=kX"
    
    session = login_and_create_session(login_url, email, password)
    if session is None:
        return

    # Change: Removed the ThreadPoolExecutor and now iterating directly over the CSV rows
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header

        for row in reader:  # Change: Loop through each row in the CSV
            song_name, download_link = row
            output_file = os.path.join(download_folder, f"{song_name}.mp3")
            download_song(session, download_link, output_file)  # Change: Call download directly

if __name__ == "__main__":
    # Example of triggering the download manually
    csv_file = "path/to/your/csv_file.csv"
    download_folder = "path/to/your/download/folder"
    trigger_download_from_csv(csv_file, download_folder)
