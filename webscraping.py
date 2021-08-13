from bs4.builder import TreeBuilderRegistry
from pandas.core.frame import DataFrame
import requests
from bs4 import BeautifulSoup
import csv
import time
import pandas as pd

GET_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"

# 98 table rows in the html page
scraped_data = []
d = []
headers = ['Name', 'Distance', 'Mass', 'Radius', 'Luminosity', "Star-Links"]

print('--------- This program scrapes data of stars. ----------')
print('--------- If you want to end the program, click the combination "Control + C" !. --------- ')


def scraper():

    requestToWeb = requests.get(GET_URL)
    time.sleep(5)

    # for each in range(1, 2):
    garlicSoup = BeautifulSoup(requestToWeb.content, 'html.parser')

    superscript = garlicSoup.find_all('sup')
    span = garlicSoup.find_all('span')

    for s in superscript:
        s.decompose()

    for sp in span:
        sp.decompose()

    # table = garlicSoup.find_all('table', attrs = {'class', 'wikitable sortable jquery-tablesorter'})

    for index1, each_tr in enumerate(garlicSoup.find_all('tr')):
        temp_list = []

        td_items = each_tr.find_all('td')

    # print(td_items)

        for index, item in enumerate(td_items):
            if index == 1:
                try:
                    temp_list.append(item.find_all('a')[0].contents[0])
                except:
                    # try:
                    temp_list.append(item.contents[0])
                    # except:
                    #     temp_list.append(item.content[0])
            elif index == 3:
                try:
                    temp_list.append(item.contents[0] + ' ' + 'Light-Years')
                except:
                    print('AGH!')
            elif index == 5:
                try:
                    if item.contents[0] == '?':
                        temp_list.append('Un-referred')
                    else:
                        temp_list.append(item.contents[0])
                except:
                    print("Whoops.")
            elif index == 6:
                try:
                    temp_list.append(item.contents[0])
                except:
                    print("AHA!")
            elif index == 7:
                try:
                    temp_list.append(item.contents[0])
                except:
                    print('???')

        for ind, it in enumerate(td_items):
            if ind == 1:
                try:
                    temp_list.append('https://en.wikipedia.org' +
                                     it.find_all('a', href=True)[0]['href'])
                except:
                    temp_list.append('Hyperlink-station yet to be built!')

        # print(temp_list)
        scraped_data.append(temp_list)


scraper()


for index, items in enumerate(scraped_data):
    newElement = scraped_data[index]
    newElement = [item.replace('\n', '') for item in newElement]
    newElement = newElement[:]

    d.append(newElement)

with open('gottenData.csv', 'w', encoding='utf-8') as j:
    writer = csv.writer(j)
    writer.writerow(headers)
    writer.writerows(d)

# with open('GottenStarData.csv', 'w', encoding='utf-8') as b:
#     wr = csv.writer(b)
#     wr.writerows(d)

# ask = input(
#     "What star's information would you like? Type in the star name - ")
# ask = ask.capitalize()


def getInformation(info):
    dataFrame = pd.read_csv('gottenData.csv')
    # data = pd.read_csv('GottenStarData.csv')

    for i in range(len(dataFrame) - 1):
        if info == dataFrame["Name"][i]:
            radius = dataFrame['Radius'][i].replace('´', '')
            # mass = dataFrame['Mass'][i].replace('<', '')
            print(str(dataFrame['Name'][i]) + ',' + ' ' + 'Mass : {}'.format(dataFrame['Mass'][i])
                  + ' ' + 'Suns' + ',' + ' ' + 'Star-Link : ' +
                  ' ' + dataFrame['Star-Links']
                  [i] + ',' + ' ' + 'Luminosity : {}'.format(dataFrame['Luminosity'][i] + ' ' + 'Suns') + ',' + ' ' + 'Radius : {}'.format(radius) + ' ' + 'Suns')

            print(' ')
            print('       Data web-scraped from wikipedia      ')


while 1 == 1:
    ask = input(
        "What star's information would you like? Type in the star name - ")

    if ask.islower():
        ask = ask.capitalize()

    getInformation(ask)
    time.sleep(2)
