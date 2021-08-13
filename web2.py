
import requests
from bs4 import BeautifulSoup

import time
import pandas as pd

GET_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

# 98 table rows in the html page
scraped_data = []
d = []
headers = ['Star_name', 'Radius', 'Mass', 'Distance_Data']
# star name, radius, mass and distance data

print('--------- This program scrapes data of dwarf stars. ----------')
print('--------- If you want to end the program, click the combination "Control + C" !. --------- ')

td_items = 0
dataframe2 = 0


def scraper():

    requestToWeb = requests.get(GET_URL)
    time.sleep(5)

    garlicSoup = BeautifulSoup(requestToWeb.content, 'html.parser')

    tables = garlicSoup.find_all('table')
    tr_data = tables[7].find_all('tr')

    temp_list = []

    for each_tr in tr_data:
        td_items = each_tr.find_all('td')

        for index, row in enumerate(td_items):
            try:
                temp_list.append(row)
            except:
                temp_list.append(row.text)

    star_name = []
    radius = []
    distance = []
    mass = []
    for i in range(0, len(temp_list)):
        print(temp_list[i].text)
        star_name.append(temp_list[i][0].text)
        distance.append(temp_list[i][5])
        radius.append(temp_list[i][7])
        mass.append(temp_list[i][8])
    dataframe = pd.DataFrame(list(zip(star_name, distance, mass, radius)), columns=[
                             'Star Name', 'Distance', 'Mass', 'Radius'])

    return dataframe


dfOutPut = scraper()

dfOutPut.to_csv("DwarfPlanets.csv")
