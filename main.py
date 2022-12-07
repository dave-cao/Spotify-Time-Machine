# Spotify playlist

import os
from pprint import pprint

import requests
import spotipy
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()


# POPULATE SONG NAMES FROM YEAR
user_year = input(
    "Which year do you want to travel to? Type the date in this formay YYYY-MM-DD: "
)
YEAR = user_year[:4]
billboard_endpoint = f"https://www.billboard.com/charts/hot-100/{user_year}/"

response = requests.get(billboard_endpoint)

song_page = response.text

soup = BeautifulSoup(song_page, "html.parser")

titles = soup.find_all(
    name="h3",
    class_="a-no-trucate",
    id="title-of-a-story",
)


# resulting titles
title_list = [title.get_text().strip() for title in titles]

# INTERACTING WITH SPOTIFY API
scope = "user-library-read playlist-modify-public"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=os.environ["SPOTIFY_CLIENT_ID"],
        client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
        redirect_uri=os.environ["SPOTIFY_REDIRECT_URI"],
    )
)


# Populating list with song URI's from top 100 songs from x-year
uri_list = []
for title in title_list:
    try:
        song_search = sp.search(q=f"track:{title} year:{YEAR}", type="track", limit=1)[
            "tracks"
        ]["items"][0]["uri"]
        print(f"Fetching...{song_search}")
        uri_list.append(song_search)
    except IndexError:
        print(f"Couldn't find song: {title}")
        continue

# Create a playlist for user with songs fetched
user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{user_year} Billboard 100",
    public=True,
    description="I created this playlist with API and python!",
)
playlist_id = playlist["id"]

# Add tracks to playlist
print("Putting tracks into playlist...")
sp.playlist_add_items(playlist_id, uri_list)

print("Done")
