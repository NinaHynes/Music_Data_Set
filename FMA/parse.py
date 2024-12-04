from bs4 import BeautifulSoup
from typing import List, Tuple

def extract_genres(html_content: str) -> List[Tuple[str, str]]:
    """Extract music genres and their URLs from the HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    genres = []
    for li in soup.find_all('li'):
        span = li.find('span')
        a = li.find('a', href=True)
        if span and a:
            genre_name = span.get_text(strip=True)
            genre_url = a['href']
            if not genre_url.startswith('http'):
                genre_url = f"https://freemusicarchive.org{genre_url}"
            genres.append((genre_name, genre_url))
    return genres
