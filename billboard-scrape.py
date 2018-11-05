import requests
import time
import timing
import datetime
from bs4 import BeautifulSoup
import pandas as pd

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

def top_song_data(base_url, date):
    r = requests.get('https://www.billboard.com/charts/' + base_url + '/' + date)
    s = BeautifulSoup(r.text, 'html.parser')

    title = s.find('div', class_='chart-number-one__title')
    artist = s.find('div', class_="chart-number-one__artist")
    last_week = s.find('div', class_='chart-number-one__last-week')
    weeks = s.find('div', class_='chart-number-one__weeks-on-chart')

    artist_list.append(artist.text.strip())  # BB includes line breaks around artist
    title_list.append(title.text)
    peak_list.append(1)
    weeks_list.append(weeks.text)

    if not last_week:
        last_week_list.append(1)
    else:
        last_week_list.append(last_week.text)

def chart_song_data(baseUrl, date):
    r = requests.get('https://www.billboard.com/charts/' + baseUrl + '/' + date)
    s = BeautifulSoup(r.text, 'html.parser')

    songs = s.findAll('div', class_='chart-list-item')
    for song in songs:
        artist = song.find(class_='chart-list-item__artist').text
        title = song.find('span', class_='chart-list-item__title-text').text

        stat = song.find(class_='chart-list-item__stats-cell')
        if not stat:
            last_week = 'N/A'
            peak = str(songs.index(song) + 2)
            weeks = 1
        else:
            last_week = song.find(class_='chart-list-item__last-week').text
            if last_week == '-':
                last_week = 'N/A'

            peak = song.find(class_='chart-list-item__weeks-at-one').text
            weeks = song.find(class_='chart-list-item__weeks-on-chart').text

        artist_list.append(artist.strip())
        title_list.append(title.strip())
        last_week_list.append(last_week)
        peak_list.append(peak)
        weeks_list.append(weeks)

saturday_list = date_gen('1961-12-25', None, 'Saturday')
monday_list = date_gen('1958-08-04', '1961-12-25', 'Monday')
dates_list = [item for sublist in [saturday_list + monday_list] for item in sublist]

output = pd.Series(dates_list)
output.to_csv('datelist.csv', index=False)

df = pd.DataFrame(columns=['Rank', 'Date', 'Artist', 'Title', 'Last Week',
                           'Peak Rank', 'Weeks on Chart'])

for date in dates_list[0:1088]:
    artist_list, title_list, last_week_list, peak_list, weeks_list = ([] for i in range(5))

    top_song_data('hot-100', date)
    chart_song_data('hot-100', date)
    print(str(date) + '|' + str(dates_list.index(date)))

    df['Rank'] = [i for i in range(1, 101)]
    df['Date'] = [date for i in range(100)]
    df['Artist'] = artist_list
    df['Title'] = title_list
    df['Combined'] = df['Artist'] + ' ' + df['Title']
    df['Last Week'] = last_week_list
    df['Peak Rank'] = peak_list
    df['Weeks on Chart'] = weeks_list

    df.to_csv('billboard-songs.csv', mode='a', header=False, index=False)
