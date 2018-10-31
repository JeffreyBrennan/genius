import requests
import csv
import time
import timing
import json
import datetime
from bs4 import BeautifulSoup
import pandas as pd
# create genius link / test w/ genius website
# classify genre
# output to table / include source (genius hot 100 / billboard) etc

def date_gen(start, end, day):
    dates_list = []

    if day == 'Monday':
        start_date = datetime.datetime.strptime(start, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end, '%Y-%m-%d').date()

        start_mod = 1

    elif day == 'Saturday':
        date_now = datetime.datetime.now()

        start_date = datetime.datetime.strptime(start, '%Y-%m-%d').date()
        end_date = (date_now + datetime.timedelta(days=(5 - date_now.weekday()))).date()

        start_mod = 0

    delta = end_date - start_date
    weekCount = delta.days // 7

    for i in range(start_mod, weekCount + start_mod):
        dayint = i * 7
        week = (end_date - datetime.timedelta(days=dayint)).strftime('%Y-%m-%d')
        dates_list.append(week)
    return dates_list


def getTopSong(baseUrl, date):
    r = requests.get('https://www.billboard.com/charts/' + baseUrl + '/' + date)
    s = BeautifulSoup(r.text, 'html.parser')

    topSong = s.find('div', class_='chart-number-one__info')
    title = topSong.find('div', class_='chart-number-one__title')
    artist = topSong.find('div', class_="chart-number-one__artist")
    weeks = topSong.find('div', class_='chart-number-one__weeks-on-chart')
    lastWeek = topSong.find('div', class_='chart-number-one__last-week')

    if not lastWeek:
        lastWeekList.append(1)
    else:
        lastWeekList.append(lastWeek.text)

    artistList.append(artist.text)
    titleList.append(title.text)

    peakList.append(1)
    weeksList.append(weeks.text)

def getSongData(baseUrl, date):
    r = requests.get('https://www.billboard.com/charts/' + baseUrl + '/' + date)
    s = BeautifulSoup(r.text, 'html.parser')

    songs = s.findAll('div', class_='chart-list-item')
    for song in songs:
        artist = song.find(class_='chart-list-item__artist')
        title = song.find('span', class_='chart-list-item__title-text')

        artistList.append(artist.text)
        titleList.append(title.text)

        stat = song.findAll(class_='chart-list-item__stats-cell')

        if not stat:
            lastWeekList.append('N/A')
            peakList.append(songs.index(song) + 2)
            weeksList.append(1)
        else:
            for item in stat:
                for lastWeek in item(class_='chart-list-item__last-week'):
                    lastWeekList.append(lastWeek.text)
                for peak in item(class_='chart-list-item__weeks-at-one'):
                    peakList.append(peak.text)
                for weeks in item(class_='chart-list-item__weeks-on-chart'):
                    weeksList.append(weeks.text)

def getDate(baseUrl, date):
    r = requests.get('https://www.billboard.com/charts/' + baseUrl + '/' + date)
    s = BeautifulSoup(r.text, 'html.parser')

    lastWeek = s.find('li', class_='dropdown__date-selector-option')
    for link in lastWeek('a'):
        if link.has_attr('href'):
            getDate.info = link['href']
            # links.append(link['href'])

def infoChoice(choice):

    charts = ['hot-100', 'billboard-200']

    if choice == 1:
        path = 'C:/Users/jeffb/Documents/Python/webPrograms/webScraping/ \
                lyrics/output/billboard-songs/'

        for i in dates_list:
            getDate(charts[0], i)
            getTopSong(charts[0], i)
            getSongData(charts[0], i)

            dateCorrection = str(int(getDate.info[-1]) + 7)
            date = (getDate.info[16:-1] + dateCorrection)

            artistList = [x.strip() for x in artistList]
            titleList = [x.strip() for x in titleList]

            print(str(i) + '/' + len(dates_list))

            with open(path + date + '-billboard-100-songs.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(zip(['Rank'], ['Week'], ['Artist'], ['Song Title'],
                                     ['Last_Week'], ['Peak_Position'], ['Chart_Weeks']))

                writer.writerows(zip((i + 1 for i in range(99)),
                                 (date for i in range(100)),
                                 artistList,
                                 titleList,
                                 lastWeekList,
                                 peakList,
                                 weeksList))

    elif choice == 2:
        path = 'C:/Users/jeffb/Documents/Python/webPrograms/webScraping/ \
                lyrics/output/billboard-albums/'

        for i in dates_list:
            # getDate(charts[1], i)
            getTopSong(charts[1], i)
            getSongData(charts[1], i)

        # dateCorrection = str(int(getDate.info[-1])+7)
        # date = (getDate.info[22:-1] + dateCorrection)

        artistList = [i.strip() for i in artistList]
        titleList = [i.strip() for i in titleList]

        with open(path + date + '-billboard-200-albums.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(zip(['Rank'], ['Week'], ['Artist'], ['Album Title'],
                                 ['Last_Week'], ['Peak_Position'], ['Chart_Weeks']))

            writer.writerows(zip((i + 1 for i in range(199)),
                             (date for i in range(200)),
                             artistList,
                             titleList,
                             lastWeekList,
                             peakList,
                             weeksList))

    else:
        print('invalid input')

# 1: Get song data
# 2: Get album data
###
# infoChoice(1)
###

path = 'C:/Users/jeffb/Documents/Python/webPrograms/webScraping/genius/output/billboard-songs/'

# Billboard began using Saturdays as start of the week on 12-25-1961
saturday_list = date_gen('1961-12-25', None, 'Saturday')
monday_list = date_gen('1958-08-04', '1961-12-25', 'Monday')
dates_list = [item for sublist in [saturday_list + monday_list] for item in sublist]

output = pd.Series(dates_list)
output.to_csv('datelist.csv', index=False)


for date in dates_list:
    artistList, titleList, lastWeekList, peakList, weeksList = ([] for i in range(5))
    getTopSong('hot-100', date)
    getSongData('hot-100', date)

    # dateCorrection = str(int(getDate.info[-1])+7)
    # date = (getDate.info[16:-1] + dateCorrection)

    artistList = [x.strip() for x in artistList]
    titleList = [x.strip() for x in titleList]

    print(date)

    with open(path + 'all-billboard-100-songs.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        # writer.writerows(zip(['Rank'], ['Week'], ['Artist'], ['Song Title'], \
        #                 ['Last_Week'], ['Peak_Position'], ['Chart_Weeks']))

        writer.writerows(zip((i for i in range(1, 101)),
                         (date for i in range(100)),
                         artistList,
                         titleList,
                         lastWeekList,
                         peakList,
                         weeksList))
