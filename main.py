import os

import requests
import spotipy
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

from get_date import get_random_date

load_dotenv()


def main():
    user_year = (
        input(
            "Which year do you want to travel to? Type the date in this format YYYY-MM-DD: "
        )
        or get_random_date()
    )
    YEAR = user_year[:4]
    billboard_endpoint = f"https://www.billboard.com/charts/hot-100/{user_year}/"

    # get the webpage
    response = requests.get(billboard_endpoint)
    song_page = response.text

    # Start scraping for all the titles
    soup = BeautifulSoup(song_page, "html.parser")
    titles = soup.find_all(name="h3", class_="a-no-trucate", id="title-of-a-story")
    title_list = [title.get_text().strip() for title in titles]

    # Connect with spotify api
    # authenticating spotify acc
    scope = "user-library-read playlist-modify-public"
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope,
            client_id=os.environ["SPOTIFY_CLIENT_ID"],
            client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
            redirect_uri=os.environ["SPOTIFY_REDIRECT_URI"],
        )
    )

    # Populating list with song URI's from top 100 songs from x-year from spotify
    uri_list = []
    for title in title_list:
        try:
            # grabs song uri from title and year
            song_search = sp.search(
                q=f"track:{title} year:{YEAR}", type="track", limit=1
            )["tracks"]["items"][0]["uri"]
            print(f"Fetching...{song_search}")
            uri_list.append(song_search)

        # If we couldn't find song
        except IndexError:
            print(f"Couldn't find song: {title}")
            continue

    # Create an empty playlist
    user_id = sp.current_user()["id"]
    playlist = sp.user_playlist_create(
        user=user_id,
        name=f"{user_year} Billboard 100",
        public=True,
        description="I created this playlist with API and python!",
    )
    playlist_id = playlist["id"]

    # Add tracks to the newly created playlist
    print("Putting tracks into playlist...")
    sp.playlist_add_items(playlist_id, uri_list)
    print("Dont")


if __name__ == "__main__":
    main()
