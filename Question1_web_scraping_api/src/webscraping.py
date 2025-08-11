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