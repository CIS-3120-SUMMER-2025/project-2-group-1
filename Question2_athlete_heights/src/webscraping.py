# Importing Libraries
import requests
from bs4 import BeautifulSoup

#Setting the URLs for the men's volleyball teams 

city_college_of_ny='https://ccnyathletics.com/sports/mens-volleyball/roster?view=2'
lehman_college='https://lehmanathletics.com/sports/mens-volleyball/roster?view=2'
brooklyn_college='https://www.brooklyncollegeathletics.com/sports/mens-volleyball/roster?view=2'
john_jay_college='https://johnjayathletics.com/sports/mens-volleyball/roster?view=2'
baruch_college='https://athletics.baruch.cuny.edu/sports/mens-volleyball/roster?view=2'
medgar_evers_college='https://mecathletics.com/sports/mens-volleyball/roster?view=2'
hunter_college='https://www.huntercollegeathletics.com/sports/mens-volleyball/roster'
york_college='https://yorkathletics.com/sports/mens-volleyball/roster'
ball_state='https://ballstatesports.com/sports/mens-volleyball/roster'

#Setting the URLs for the women's volleyball teams 
bmcc='https://bmccathletics.com/sports/womens-volleyball/roster?view=2'
york_college_women='https://yorkathletics.com/sports/womens-volleyball/roster'
hostos_cc='https://hostosathletics.com/sports/womens-volleyball/roster?view=2'
bronx_cc='https://bronxbroncos.com/sports/womens-volleyball/roster/2021?view=2'
queens_college='https://queensknights.com/sports/womens-volleyball/roster?view=2'
augusta_college='https://augustajags.com/sports/wvball/roster'
flagler_college='https://flaglerathletics.com/sports/womens-volleyball/roster?view=2'
usc_aiken='https://pacersports.com/sports/womens-volleyball/roster'
penn_state_lock_haven='https://www.lockhavenathletics.com/sports/womens-volleyball/roster'