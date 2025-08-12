#import libaries 
import requests 
from bs4 import BeautifulSoup
# need this for the dataframe creation
import pandas as pd

#set url 
url = 'https://www.billboard.com/charts/hot-100/'

# # headers Source: https://www.zenrows.com/blog/web-scraping-headers#user-agent
headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.9',
  'Connection': 'keep-alive'
  }

# # making a request to the server
page = requests.get(url, headers= headers)

#make a request to the server
page = requests.get(url)
#check status code
page.status_code

#import raw html into beautifulsoup
soup = BeautifulSoup(page.content,'html.parser')

# Find all divs for each chart row (each song) so i can see the tags
parent = soup.find_all('div', class_='o-chart-results-list-row-container')
songs = []
artists = []

for title in parent:
    # Find song title in <h3> with class 'c-title'
    song_tag = title.find('h3', class_='c-title')
    # Find artist name in <span> with class 'a-no-trucate'
    artist_tag = title.find('span', class_='a-no-trucate')

    if song_tag and artist_tag:
        song = song_tag.get_text(strip=True)
        artist = artist_tag.get_text(strip=True)
        songs.append(song)
        artists.append(artist)
        print('Song:', song, '| Artist:', artist)
billboard_data={
     'Song': songs,
    'Artist': artists
}
DF1= pd.DataFrame(billboard_data)
print(DF1.head())
DF1.to_csv('billboard_songs.csv', index=False)

import time, requests, pandas as pd

DF1_PATH = "billboard_songs.csv"
OUT_PATH = "df2_itunes.csv"

def search_itunes(song, artist):
    term = f"{song} {artist}"
    url = "https://itunes.apple.com/search"
    params = {"term": term, "entity": "song", "limit": 1}
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        j = r.json()
        if j.get("resultCount", 0) == 0:
            return {
                "match_ok": False,
                "trackId": None,
                "collectionName": None,
                "primaryGenreName": None,
                "releaseDate": None,
                "trackTimeMillis": None,
                "previewUrl": None,
                "trackViewUrl": None,
            }
        d = j["results"][0]
        return {
            "match_ok": True,
            "trackId": d.get("trackId"),
            "collectionName": d.get("collectionName"),
            "primaryGenreName": d.get("primaryGenreName"),
            "releaseDate": d.get("releaseDate"),
            "trackTimeMillis": d.get("trackTimeMillis"),
            "previewUrl": d.get("previewUrl"),
            "trackViewUrl": d.get("trackViewUrl"),
        }
    except Exception:
        return {
            "match_ok": False,
            "trackId": None,
            "collectionName": None,
            "primaryGenreName": None,
            "releaseDate": None,
            "trackTimeMillis": None,
            "previewUrl": None,
            "trackViewUrl": None,
        }

df1 = pd.read_csv(DF1_PATH)
records = []
for _, row in df1.iterrows():
    meta = search_itunes(row["Song"], row["Artist"])
    meta["Song"] = row["Song"]
    meta["Artist"] = row["Artist"]
    records.append(meta)
    time.sleep(0.1)   # be polite to API

df2 = pd.DataFrame(records, columns=[
    "Song","Artist","match_ok","trackId","collectionName",
    "primaryGenreName","releaseDate","trackTimeMillis",
    "previewUrl","trackViewUrl"
])
df2.to_csv(OUT_PATH, index=False)
print(df2.shape, "saved to", OUT_PATH)

import sqlite3

df3 = pd.merge(df1, df2, on=["Song", "Artist"], how="inner")

print("\nMerged DataFrame (DF3):")
print(df3.head())

print("\nDescriptive statistics:")
print(df3.describe(include="all"))
df3.to_csv("df3_combined.csv", index=False)

conn = sqlite3.connect("songs.db")
df3.to_sql("df3_table", conn, if_exists="replace", index=False)
conn.commit()
conn.close()

print("\nDF3 successfully saved to SQL database 'songs.db' in table 'df3_table'")
