import requests, csv, time, timing, json
from bs4 import BeautifulSoup
 
## create genius link / test w/ genius website 
## classify genre 
# output to table / include source (genius hot 100 / billboard) etc

artistList, titleList, lastWeekList, peakList, weeksList =([] for i in range(5))

def getTopSong(url):
    r = requests.get('https://www.billboard.com/charts/'+url)
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

def getSongData(url):
    r = requests.get('https://www.billboard.com/charts/'+url)
    s = BeautifulSoup(r.text, 'html.parser')

    songs = s.findAll('div',class_='chart-list-item')
    for song in songs:
        artist = song.find(class_='chart-list-item__artist')
        title = song.find('span', class_='chart-list-item__title-text')

        artistList.append(artist.text)
        titleList.append(title.text)
        
        stat = song.findAll(class_='chart-list-item__stats-cell')

        if not stat: 
            lastWeekList.append('N/A')
            peakList.append(songs.index(song)+2)
            weeksList.append(1)
        else:
            for item in stat:
                for lastWeek in item(class_='chart-list-item__last-week'):
                    lastWeekList.append(lastWeek.text)
                for peak in item(class_='chart-list-item__weeks-at-one'):
                    peakList.append(peak.text)
                for weeks in item(class_='chart-list-item__weeks-on-chart'):
                    weeksList.append(weeks.text)
    
def getDate(url):
    r = requests.get('https://www.billboard.com/charts/'+url)
    s = BeautifulSoup(r.text, 'html.parser')

    lastWeek = s.find('li', class_='dropdown__date-selector-option')
    for link in lastWeek('a'):
        if link.has_attr('href'):
            getDate.info = link['href']
            # links.append(link['href'])

def infoChoice (choice):
    
    charts = ['hot-100', 'billboard-200']
    
    if choice == 1:
        path = 'C:/Users/jeffb/Documents/Python/webPrograms/webScraping/ \
                genius/output/billboard-songs/'

        getDate(charts[0])
        getTopSong(charts[0])
        getSongData(charts[0])

        dateCorrection = str(int(getDate.info[-1])+7)
        date = (getDate.info[16:-1] + dateCorrection)
        
        artistList = [i.strip() for i in artistList]
        titleList = [i.strip() for i in titleList]


        with open(path + date + '-billboard-100-songs.csv','w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(zip(['Rank'], ['Week'], ['Artist'], ['Song Title'], \
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
                genius/output/billboard-albums/'

        getDate(charts[1])
        getTopSong(charts[1])
        getSongData(charts[1])

        dateCorrection = str(int(getDate.info[-1])+7)
        date = (getDate.info[22:-1] + dateCorrection)

        artistList = [i.strip() for i in artistList]
        titleList = [i.strip() for i in titleList]


        with open(path + date + '-billboard-200-albums.csv','w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(zip(['Rank'], ['Week'], ['Artist'], ['Album Title'], \
                            ['Last_Week'], ['Peak_Position'], ['Chart_Weeks']))

            writer.writerows(zip((i + 1 for i in range(199)),
                            (date for i in range(200)),
                            artistList, 
                            titleList,
                            lastWeekList,
                            peakList,
                            weeksList))

    else:
        print ('invalid input')

### 1: Get song data
### 2: Get album data
###
infoChoice(2)
###