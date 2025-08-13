## ALL MERGED Q1-Q9 ##

import time
import requests
from bs4 import BeautifulSoup
import pandas as pd


## QUESTION 1 ##

# URLs of schools' men's swim rosters
urls = {
    "College of Staten Island": "https://csidolphins.com/sports/mens-swimming-and-diving/roster",
    "York College": "https://yorkathletics.com/sports/mens-swimming-and-diving/roster",
    "Baruch College": "https://athletics.baruch.cuny.edu/sports/mens-swimming-and-diving/roster",
    "Brooklyn College": "https://www.brooklyncollegeathletics.com/sports/mens-swimming-and-diving/roster",
    "Lindenwood University": "https://lindenwoodlions.com/sports/mens-swimming-and-diving/roster",
    "Mckendree University": "https://mckbearcats.com/sports/mens-swimming-and-diving/roster",
    "Ramapo College": "https://ramapoathletics.com/sports/mens-swimming-and-diving/roster",
    "SUNY Oneota": "https://oneontaathletics.com/sports/mens-swimming-and-diving/roster",
    "SUNY Binghamton": "https://bubearcats.com/sports/mens-swimming-and-diving/roster/2021-22",
    "Albright College": "https://albrightathletics.com/sports/mens-swimming-and-diving/roster/2021-22",
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_html(url):
    tries = 3
    for _ in range(tries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except:
            time.sleep(1)
    return None

def clean_text(text):
    if text:
        return ' '.join(text.split())
    return None

def find_height(text):
    if not text:
        return None

    text = text.lower().replace(' ', '')

    # Check for cm (like 185cm)
    if "cm" in text:
        num_str = ''
        for char in text:
            if char.isdigit():
                num_str += char
            elif num_str:
                break
        if num_str.isdigit():
            return num_str + " cm"

    # Check for 6-1 style height
    if '-' in text:
        parts = text.split('-')
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            return parts[0] + '-' + parts[1]

    # Check for 6'1 or 6'1" style height
    if "'" in text:
        parts = text.split("'")
        if len(parts) == 2:
            feet = parts[0]
            inch = parts[1].replace('"','')
            if feet.isdigit() and inch.isdigit():
                return feet + "'" + inch + '"'

    return None

def height_to_inches(height):
    if not height:
        return None

    height = height.lower().replace(' ', '')

    if 'cm' in height:
        try:
            cm = int(''.join(filter(str.isdigit, height)))
            inches = round(cm / 2.54)
            return inches
        except:
            return None

    if '-' in height:
        parts = height.split('-')
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            return int(parts[0]) * 12 + int(parts[1])

    if "'" in height:
        parts = height.split("'")
        if len(parts) == 2 and parts[0].isdigit() and parts[1].replace('"','').isdigit():
            feet = int(parts[0])
            inches = int(parts[1].replace('"',''))
            return feet * 12 + inches

    return None

def inches_to_height_string(inches):
    feet = int(inches) // 12
    inch = int(inches) % 12
    return f"{feet}'{inch}\""

all_data = []

for school, url in urls.items():
    print(f"Scraping {school}...")
    html = get_html(url)
    if not html:
        print(f"Failed to get data from {school}")
        continue

    soup = BeautifulSoup(html, 'html.parser')
    players = []

    cards = soup.select('li.sidearm-roster-player, tr.sidearm-roster-player, .sidearm-roster-player')
    if not cards:
        cards = soup.select("[class*=sidearm][class*=roster] .sidearm-roster-player, [class*=sidearm-roster-player]")

    for card in cards:
        name_tag = card.select_one('.sidearm-roster-player-name a') or card.select_one('.sidearm-roster-player-name')
        name = clean_text(name_tag.get_text()) if name_tag else None

        height_tag = card.select_one('.sidearm-roster-player-height') or card.select_one('[data-player-height]') or card.select_one('[class*=height]')
        height = None
        if height_tag:
            height = find_height(clean_text(height_tag.get_text()))

        if not height:
            text = clean_text(card.get_text(' '))
            height = find_height(text)

        if name:
            players.append({'school': school, 'name': name, 'height': height})

    print(f"Found {len(players)} players for {school}")
    all_data.extend(players)
    time.sleep(1)

df = pd.DataFrame(all_data)

# Convert height strings to inches
df['height_in'] = df['height'].apply(height_to_inches)

# Calculate average height ignoring missing
avg_height = int(df['height_in'].dropna().mean())
print(f"Average height in inches: {avg_height}")

# Fill missing heights with average
df['height_in'] = df['height_in'].fillna(avg_height)

# Convert back to height string format
df['height'] = df['height_in'].apply(inches_to_height_string)
df = df.drop(columns=['height_in'])
df.to_csv('mens_swimming.csv', index=False)
print("Data saved to mens_swimming.csv")

## QUESTION 2 ##

# List of colleges and their roster URLs
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

def get_text_safe(tag):
    if tag:
        return tag.get_text().strip()
    else:
        return None

# Function to convert height like '5-8' or '5'8"' to inches
def height_to_inches(height):
    if not height or height.lower() == 'nan':
        return None

    # Try to split by '-' or "'"
    if '-' in height:
        parts = height.split('-')
    elif "'" in height:
        parts = height.split("'")
    else:
        # If just a number (inches)
        if height.isdigit():
            return int(height)
        else:
            return None

    try:
        feet = int(parts[0])
        inches = int(parts[1].replace('"', '').strip())
        return feet * 12 + inches
    except:
        return None

# Convert inches back to string like 5'8" (no decimals)
def inches_to_height(inches):
    feet = int(inches) // 12
    inch = int(inches) % 12
    return f"{feet}'{inch}\""

def scrape_roster(college_name, url):
    print(f"Starting to scrape {college_name}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    players = soup.find_all('li', class_='sidearm-roster-player')

    results = []
    for player in players:
        name_tag = player.find('div', class_='sidearm-roster-player-name')
        if not name_tag:
            name_tag = player.find('span', class_='sidearm-roster-player-name')
        name = get_text_safe(name_tag) or "NaN"

        height_tag = player.find('span', class_='sidearm-roster-player-height')
        height = get_text_safe(height_tag) or "NaN"

        results.append({'College': college_name, 'Name': name, 'Height': height})

    return results

all_players = []

for college, url in colleges:
    try:
        players = scrape_roster(college, url)
        all_players.extend(players)
        time.sleep(1)  # be nice to the servers
    except Exception as e:
        print(f"Could not scrape {college}: {e}")

df = pd.DataFrame(all_players)

# Convert height strings to inches
df['Height_in'] = df['Height'].apply(height_to_inches)

# Calculate average height (ignore missing)
avg_height = int(df['Height_in'].dropna().mean())
print(f"Average height in inches: {avg_height}")

# Replace missing heights with average
df['Height_in'] = df['Height_in'].fillna(avg_height)

# Convert back to height string without decimals
df['Height'] = df['Height_in'].apply(inches_to_height)

# Drop temporary column
df = df.drop(columns=['Height_in'])


df.to_csv('womens_swimming.csv', index=False)
print("Saved data to womens_swimming.csv")


## QUESTION 3 ##

# URLs of men's volleyball rosters
urls = {
    "City College of New York": "https://ccnyathletics.com/sports/mens-volleyball/roster",
    "Lehman College": "https://lehmanathletics.com/sports/mens-volleyball/roster",
    "Brooklyn College": "https://www.brooklyncollegeathletics.com/sports/mens-volleyball/roster",
    "John Jay College": "https://johnjayathletics.com/sports/mens-volleyball/roster",
    "Baruch College": "https://athletics.baruch.cuny.edu/sports/mens-volleyball/roster",
    "Medgar Evers College": "https://mecathletics.com/sports/mens-volleyball/roster",
    "Hunter College": "https://www.huntercollegeathletics.com/sports/mens-volleyball/roster",
    "York College": "https://yorkathletics.com/sports/mens-volleyball/roster",
    "Ball State": "https://ballstatesports.com/sports/mens-volleyball/roster",
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_html(url):
    tries = 3
    for _ in range(tries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except:
            time.sleep(1)
    return None

def clean_text(text):
    if text:
        return ' '.join(text.split())
    return None

def find_height(text):
    if not text:
        return None

    text = text.lower().replace(' ', '')

    # Check for cm (like 185cm)
    if "cm" in text:
        num_str = ''
        for char in text:
            if char.isdigit():
                num_str += char
            elif num_str:
                break
        if num_str.isdigit():
            return num_str + " cm"

    # Check for 6-1 style height
    if '-' in text:
        parts = text.split('-')
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            return parts[0] + '-' + parts[1]

    # Check for 6'1 or 6'1" style height
    if "'" in text:
        parts = text.split("'")
        if len(parts) == 2:
            feet = parts[0]
            inch = parts[1].replace('"','')
            if feet.isdigit() and inch.isdigit():
                return feet + "'" + inch + '"'

    return None

def height_to_inches(height):
    if not height:
        return None

    height = height.lower().replace(' ', '')

    if 'cm' in height:
        try:
            cm = int(''.join(filter(str.isdigit, height)))
            inches = round(cm / 2.54)
            return inches
        except:
            return None

    if '-' in height:
        parts = height.split('-')
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            return int(parts[0]) * 12 + int(parts[1])

    if "'" in height:
        parts = height.split("'")
        if len(parts) == 2 and parts[0].isdigit() and parts[1].replace('"','').isdigit():
            feet = int(parts[0])
            inches = int(parts[1].replace('"',''))
            return feet * 12 + inches

    return None

def inches_to_height_string(inches):
    feet = int(inches) // 12
    inch = int(inches) % 12
    return f"{feet}'{inch}\""

all_data = []

for school, url in urls.items():
    print(f"Scraping {school}...")
    html = get_html(url)
    if not html:
        print(f"Failed to get data from {school}")
        continue

    soup = BeautifulSoup(html, 'html.parser')
    players = []

    # Try to find roster players with common sidearm classes or table rows
    cards = soup.select('li.sidearm-roster-player, tr.sidearm-roster-player, .sidearm-roster-player')
    if not cards:
        cards = soup.select("[class*=sidearm][class*=roster] .sidearm-roster-player, [class*=sidearm-roster-player]")

    # Special fallback for Brooklyn College table structure
    if school == "Brooklyn College" and not cards:
        table = soup.find('table', class_='sidearm-roster-table')
        if table:
            rows = table.find_all('tr')[1:]  # skip header
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 4:
                    name = clean_text(cols[1].get_text())
                    height = find_height(clean_text(cols[3].get_text()))
                    players.append({'school': school, 'name': name, 'height': height})
        all_data.extend(players)
        print(f"Found {len(players)} players for {school}")
        time.sleep(1)
        continue

    for card in cards:
        name_tag = card.select_one('.sidearm-roster-player-name a') or card.select_one('.sidearm-roster-player-name')
        name = clean_text(name_tag.get_text()) if name_tag else None

        height_tag = card.select_one('.sidearm-roster-player-height') or card.select_one('[data-player-height]') or card.select_one('[class*=height]')
        height = None
        if height_tag:
            height = find_height(clean_text(height_tag.get_text()))

        if not height:
            text = clean_text(card.get_text(' '))
            height = find_height(text)

        if name:
            players.append({'school': school, 'name': name, 'height': height})

    print(f"Found {len(players)} players for {school}")
    all_data.extend(players)
    time.sleep(1)

df = pd.DataFrame(all_data)

# Convert height strings to inches
df['height_in'] = df['height'].apply(height_to_inches)

# Calculate average height ignoring missing
if not df['height_in'].dropna().empty:
    avg_height = int(df['height_in'].dropna().mean())
else:
    avg_height = None
print(f"Average height in inches: {avg_height if avg_height else 'No height data'}")

# Fill missing heights with average if available
if avg_height:
    df['height_in'] = df['height_in'].fillna(avg_height)

# Convert back to height string format
if avg_height:
    df['height'] = df['height_in'].apply(inches_to_height_string)

df = df.drop(columns=['height_in'])
df.to_csv('mens_volleyball.csv', index=False)
print("Data saved to mens_volleyball.csv")


## QUESTION 4 ##

# URLs of women's volleyball rosters
urls = {
    "BMCC": "https://bmccathletics.com/sports/womens-volleyball/roster",
    "York College": "https://yorkathletics.com/sports/womens-volleyball/roster",
    "Hostos CC": "https://hostosathletics.com/sports/womens-volleyball/roster",
    "Bronx CC": "https://bronxbroncos.com/sports/womens-volleyball/roster/2021",
    "Queens College": "https://queensknights.com/sports/womens-volleyball/roster",
    "Augusta College": "https://augustajags.com/sports/wvball/roster",
    "Flagler College": "https://flaglerathletics.com/sports/womens-volleyball/roster",
    "USC Aiken": "https://pacersports.com/sports/womens-volleyball/roster",
    "Penn State - Lock Haven": "https://www.golhu.com/sports/womens-volleyball/roster",
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_html(url):
    tries = 3
    for _ in range(tries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except:
            time.sleep(1)
    return None

def clean_text(text):
    if text:
        return ' '.join(text.split())
    return None

def find_height(text):
    if not text:
        return None

    text = text.lower().replace(' ', '')

    if "cm" in text:
        num_str = ''
        for char in text:
            if char.isdigit():
                num_str += char
            elif num_str:
                break
        if num_str.isdigit():
            return num_str + " cm"

    if '-' in text:
        parts = text.split('-')
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            return parts[0] + '-' + parts[1]

    if "'" in text:
        parts = text.split("'")
        if len(parts) == 2:
            feet = parts[0]
            inch = parts[1].replace('"','')
            if feet.isdigit() and inch.isdigit():
                return feet + "'" + inch + '"'

    return None

def height_to_inches(height):
    if not height:
        return None

    height = height.lower().replace(' ', '')

    if 'cm' in height:
        try:
            cm = int(''.join(filter(str.isdigit, height)))
            inches = round(cm / 2.54)
            return inches
        except:
            return None

    if '-' in height:
        parts = height.split('-')
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            return int(parts[0]) * 12 + int(parts[1])

    if "'" in height:
        parts = height.split("'")
        if len(parts) == 2 and parts[0].isdigit() and parts[1].replace('"','').isdigit():
            feet = int(parts[0])
            inches = int(parts[1].replace('"',''))
            return feet * 12 + inches

    return None

def inches_to_height_string(inches):
    feet = int(inches) // 12
    inch = int(inches) % 12

    # Fix cases like 0'4" -> 4'0"
    if feet == 0 and inch >= 3:
        feet, inch = inch, 0

    return f"{feet}'{inch}\""

all_data = []

for school, url in urls.items():
    print(f"Scraping {school}...")
    html = get_html(url)
    if not html:
        print(f"Failed to get data from {school}")
        continue

    soup = BeautifulSoup(html, 'html.parser')
    players = []

    cards = soup.select('li.sidearm-roster-player, tr.sidearm-roster-player, .sidearm-roster-player')
    if not cards:
        cards = soup.select("[class*=sidearm][class*=roster] .sidearm-roster-player, [class*=sidearm-roster-player]")

    for card in cards:
        name_tag = card.select_one('.sidearm-roster-player-name a') or card.select_one('.sidearm-roster-player-name')
        name = clean_text(name_tag.get_text()) if name_tag else None

        height_tag = card.select_one('.sidearm-roster-player-height') or card.select_one('[data-player-height]') or card.select_one('[class*=height]')
        height = None
        if height_tag:
            height = find_height(clean_text(height_tag.get_text()))

        if not height:
            text = clean_text(card.get_text(' '))
            height = find_height(text)

        if name:
            players.append({'school': school, 'name': name, 'height': height})

    print(f"Found {len(players)} players for {school}")
    all_data.extend(players)
    time.sleep(1)

df = pd.DataFrame(all_data)

df['height_in'] = df['height'].apply(height_to_inches)

if not df['height_in'].dropna().empty:
    avg_height = int(df['height_in'].dropna().mean())
else:
    avg_height = None
print(f"Average height in inches: {avg_height if avg_height else 'No height data'}")

if avg_height:
    df['height_in'] = df['height_in'].fillna(avg_height)
    df['height'] = df['height_in'].apply(inches_to_height_string)

df = df.drop(columns=['height_in'])
df.to_csv('womens_volleyball.csv', index=False)
print("Data saved to womens_volleyball.csv")


## QUESTION 5 ##

def to_inches(s):
    if pd.isna(s):
        return None
    s = str(s).strip().replace('’', "'").replace('″', '"').replace('–', '-').replace('—', '-')

    # Try to parse format like 6-2 or 6'2"
    if '-' in s:
        parts = s.split('-')
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            feet = int(parts[0])
            inches = int(parts[1])
            return feet * 12 + inches

    if "'" in s:
        parts = s.split("'")
        if len(parts) == 2:
            feet = parts[0].strip()
            inches = parts[1].replace('"', '').strip()
            if feet.isdigit() and inches.isdigit():
                return int(feet) * 12 + int(inches)

    # Check for cm (e.g. 180 cm or 180cm)
    s_lower = s.lower().replace(' ', '')
    if s_lower.endswith("cm"):
        number_part = s_lower[:-2]
        try:
            cm = float(number_part)
            return cm / 2.54
        except:
            return None

    # Try to convert directly to number (inches or cm)
    try:
        val = float(s)
        if val > 100:  # assume cm
            return val / 2.54
        else:
            return val
    except:
        return None

def average_height_from_csv(path):
    df = pd.read_csv(path)
    height_col = None
    for col in df.columns:
        if "height" in col.lower() or col.lower() in ['ht', 'ht.']:
            height_col = col
            break
    if not height_col:
        return None

    heights_in = df[height_col].map(to_inches)
    valid_heights = heights_in[(heights_in >= 55) & (heights_in <= 85)]
    if valid_heights.empty:
        return None
    return round(valid_heights.mean(), 2)

files = [
    ("Men's Swimming",     "mens_swimming.csv"),
    ("Men's Volleyball",   "mens_volleyball.csv"),
    ("Women's Swimming",   "womens_swimming.csv"),
    ("Women's Volleyball", "womens_volleyball.csv"),
]

print("Average Heights (inches):")
print("-------------------------")
for label, filepath in files:
    avg = average_height_from_csv(filepath)
    print(f"{label}: {avg if avg else 'No data'}")

## QUESTION 6 ##

import csv


def height_to_inches(height):
    if not height:
        return None
    h = height.lower().replace(' ', '').replace('”', '"').replace('’', "'")
    
    if 'cm' in h:
        try:
            cm = int(''.join(filter(str.isdigit, h)))
            return round(cm / 2.54)
        except:
            return None
    
    if '-' in h:
        parts = h.split('-')
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            return int(parts[0]) * 12 + int(parts[1])
    
    if "'" in h:
        parts = h.split("'")
        if len(parts) == 2:
            feet = parts[0]
            inches = parts[1].replace('"', '')
            if feet.isdigit() and inches.isdigit():
                return int(feet)*12 + int(inches)
    
    if h.isdigit():
        return int(h)
    
    return None

def inches_to_height_string(inches):
    feet = inches // 12
    inch = inches % 12
    return f"{feet}'{inch}\""

def load_athletes(filename):
    athletes = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row.get('Name') or row.get('name')
            height_str = row.get('Height') or row.get('height')
            height_in = height_to_inches(height_str)
            if name and height_in is not None:
                athletes.append({'name': name, 'height': height_in})
    return athletes

def find_top_bottom_athletes(athletes, top_n=5):
    # Sort descending by height for tallest
    sorted_athletes = sorted(athletes, key=lambda x: x['height'], reverse=True)
    tallest = sorted_athletes[:top_n] if len(sorted_athletes) >= top_n else sorted_athletes

    # Sort ascending by height for shortest
    sorted_athletes_asc = sorted(athletes, key=lambda x: x['height'])
    shortest = sorted_athletes_asc[:top_n] if len(sorted_athletes_asc) >= top_n else sorted_athletes_asc

    return tallest, shortest


files = {
    "men_swimming": "mens_swimming.csv",
    "men_volleyball": "mens_volleyball.csv",
    "women_swimming": "womens_swimming.csv",
    "women_volleyball": "womens_volleyball.csv",
}

results = {}

for key, filepath in files.items():
    athletes = load_athletes(filepath)
    tallest, shortest = find_top_bottom_athletes(athletes, top_n=5)
    results[f"tallest_{key}"] = tallest
    results[f"shortest_{key}"] = shortest

# Print results
for key in results:
    print(f"\n{key.replace('_', ' ').title()}:")
    for athlete in results[key]:
        print(f"{athlete['name']} - {inches_to_height_string(athlete['height'])}")


## QUESTION 8 ##

import matplotlib.pyplot as plt

teams = ["Men's Swimming", "Men's Volleyball", "Women's Swimming", "Women's Volleyball"]
avg_heights = [71.19, 70.93, 65.64, 67.98]

plt.figure(figsize=(8,5))
bars = plt.bar(teams, avg_heights, color=['blue', 'orange', 'green', 'red'])

plt.title('Average Height Distribution Across Teams')
plt.ylabel('Average Height (inches)')
plt.ylim(60, 75)  # Adjust to fit data nicely

# Add labels on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.2, f'{height:.2f}', ha='center')

plt.tight_layout()
plt.savefig('average_height_distribution.png')
plt.show()

## QUESTION 9 ##

import sqlite3
import pandas as pd

# CSV file paths and their respective team labels
files = [
    ("mens_swimming.csv", "Men's Swimming"),
    ("womens_swimming.csv", "Women's Swimming"),
    ("mens_volleyball.csv", "Men's Volleyball"),
    ("womens_volleyball.csv", "Women's Volleyball"),
]

# Connect to (or create) the SQLite database
conn = sqlite3.connect("athletes.db")
cursor = conn.cursor()

# Drop the table if it exists (start fresh)
cursor.execute("DROP TABLE IF EXISTS athletes")

# Create the unified table
cursor.execute("""
CREATE TABLE athletes (
    school TEXT,
    name TEXT,
    height TEXT,
    team_type TEXT
)
""")

# Loop through CSV files and insert into DB
for csv_file, team_type in files:
    df = pd.read_csv(csv_file)

    # Rename columns to match our DB schema
    df = df.rename(columns={
        'College': 'school',
        'School': 'school',
        'Name': 'name',
        'Height': 'height'
    })

    # Keep only relevant columns if they exist
    for col in ['school', 'name', 'height']:
        if col not in df.columns:
            df[col] = None  # fill missing column

    # Add team_type column
    df['team_type'] = team_type

    # Select the correct column order
    df = df[['school', 'name', 'height', 'team_type']]

    # Append to SQL table
    df.to_sql('athletes', conn, if_exists='append', index=False)

# Commit and close
conn.commit()
conn.close()

print("All athlete data loaded into athletes.db successfully!")


 
