# Importing Libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

#Setting the URLs for the teams 
# Setting the URLs for the teams
#1-4
sports_dict={
    'volleyball_mens':[
        'https://ccnyathletics.com/sports/mens-volleyball/roster?view=2','https://lehmanathletics.com/sports/mens-volleyball/roster?view=2','https://www.brooklyncollegeathletics.com/sports/mens-volleyball/roster?view=2',
        'https://johnjayathletics.com/sports/mens-volleyball/roster?view=2','https://athletics.baruch.cuny.edu/sports/mens-volleyball/roster?view=2',
        'https://mecathletics.com/sports/mens-volleyball/roster?view=2','https://www.huntercollegeathletics.com/sports/mens-volleyball/roster?view=2',
        'https://yorkathletics.com/sports/mens-volleyball/roster',
        'https://ballstatesports.com/sports/mens-volleyball/roster'
        ],
        'volleyball_womens':[
          'https://bmccathletics.com/sports/womens-volleyball/roster?view=2',
          'https://yorkathletics.com/sports/womens-volleyball/roster',
          'https://hostosathletics.com/sports/womens-volleyball/roster?view=2',
          'https://bronxbroncos.com/sports/womens-volleyball/roster/2021?view=2',
          'https://queensknights.com/sports/womens-volleyball/roster?view=2',
          'https://augustajags.com/sports/wvball/roster?view=2',
          'https://flaglerathletics.com/sports/womens-volleyball/roster?view=2',
          'https://pacersports.com/sports/womens-volleyball/roster',
          'https://www.lockhavenathletics.com/sports/womens-volleyball/roster'
        ]
}




# Set the headers and make a request to the server
headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.9',
  'Connection': 'keep-alive'
  }

# make a request to the server
page= requests.get(sports_dict, headers=headers, verify=False)

print(page.status_code)

# look at raw html
print(page.content)
# import raw html into beautifulsoup
soup=BeautifulSoup(page.content,'html.parser')
print(soup.prettify())

# this is number 6
# the shortest and tallest

def tallest_and_shortest(sports_df,sport_name):
  # sorting ascending for shortest
  sports_df_sort_asc=sports_df.sort_values('Heights', ascending=True)
  # shortest_cutoff=sports_df_sort_asc[0:6]['Heights']
  shortest_cutoff=sports_df_sort_asc.iloc[4]['Heights']
  shortest_persons=sports_df_sort_asc[sports_df_sort_asc['Heights']<=shortest_cutoff]

# Sort descending for tallest
  sports_df_sort_desc = sports_df.sort_values('Heights', ascending=False)
  tallest_cutoff = sports_df_sort_desc.iloc[4]['Heights']  # 5th tallest height
  tallest_persons = sports_df_sort_desc[sports_df_sort_desc['Heights'] >= tallest_cutoff]

  print(f"\n{sport_name} - Shortest athletes :")
  for index, row in shortest_persons.iterrows():
        print(row['Names'], "-", row['Heights'], "inches")

  print(f"\n{sport_name} - Tallest athletes:")
  for index, row in tallest_persons.iterrows():
        print(row['Names'], "-", row['Heights'], "inches")

sports = list(sports_dict.keys())
for sport in sports:
    filename = sport + "_data.csv"
    df = pd.read_csv(filename)
    tallest_and_shortest(df, sport)
