import requests
import spotipy
import os
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

URL = f"https://www.billboard.com/charts/hot-100/{date}"
response = requests.get(URL)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")
songs = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
song_titles = [song.getText() for song in songs]

song_uris = []
year = date.split("-")[0]
for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
        print(f"{song} found.")
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{year} Memories", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print("Your playlist is ready.")
