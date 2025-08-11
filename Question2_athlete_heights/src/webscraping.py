# Importing Libraries
import requests
from bs4 import BeautifulSoup

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