import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

colleges = [
    ("College of Staten Island", "https://csidolphins.com/sports/womens-swimming-and-diving/roster"),
    ("Queens College", "https://queensknights.com/sports/womens-swimming-and-diving/roster"),
    ("York College", "https://yorkathletics.com/sports/womens-swimming-and-diving/roster"),
    ("Baruch College", "https://athletics.baruch.cuny.edu/sports/womens-swimming-and-diving/roster/2021-22?path=wswim"),
    ("Brooklyn College", "https://www.brooklyncollegeathletics.com/sports/womens-swimming-and-diving/roster"),
    ("Lindenwood University", "https://lindenwoodlions.com/sports/womens-swimming-and-diving/roster"),
    ("McKendree University", "https://mckbearcats.com/sports/womens-swimming-and-diving/roster"),
    ("Ramapo College", "https://ramapoathletics.com/sports/womens-swimming-and-diving/roster"),
    ("Kean University", "https://keanathletics.com/sports/womens-swimming-and-diving/roster"),
    ("SUNY Oneonta", "https://oneontaathletics.com/sports/womens-swimming-and-diving/roster"),
]

def safe_get_text(tag):
    if tag and tag.get_text():
        return tag.get_text().strip()
    return None

def scrape_roster(college_name, url):
    print(f"Scraping {college_name}...")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    players = soup.find_all('li', class_='sidearm-roster-player')
    rows = []

    for player in players:
        name_tag = player.find('div', class_='sidearm-roster-player-name') or \
                   player.find('span', class_='sidearm-roster-player-name')
        name = safe_get_text(name_tag) or "NaN"

        height_tag = player.find('span', class_='sidearm-roster-player-height')
        height = safe_get_text(height_tag) or "NaN"

        rows.append({'College': college_name, 'Name': name, 'Height': height})

    return rows

all_rows = []

for college, url in colleges:
    try:
        rows = scrape_roster(college, url)
        all_rows.extend(rows)
        time.sleep(1)
    except Exception as e:
        print(f"Error scraping {college}: {e}")

df = pd.DataFrame(all_rows)
df.to_csv('womens_swimming.csv', index=False)
print("Data saved to 'womens_swimming.csv'")
