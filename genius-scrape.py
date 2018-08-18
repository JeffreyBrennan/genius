import requests, csv, time, timing, json
from bs4 import BeautifulSoup

releasedList, linkList, songList, viewList, lyricsList, artistList, titleList, rankList, dateList = ([] for i in range(9))
page = [1,2]
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

checked = time.time()

def getInfo (page):
    r = requests.get('https://genius.com/api/songs/chart?page='+str(page)+'&per_page=50&time_period=day')
    data = json.loads(r.content.decode())
    x = 0 

    while x < 50:
        link = data['response']['chart_items'][x]['item']['path']
        songID = data['response']['chart_items'][x]['item']['id']
        views = data['response']['chart_items'][x]['item']['stats']['pageviews']
        artist = data['response']['chart_items'][x]['item']['primary_artist']['name']       
        title = data['response']['chart_items'][x]['item']['title']

        linkList.append(link)
        songList.append(songID)
        viewList.append(views)
        dateList.append(checked)
        artistList.append (artist)
        titleList.append(title)
        
        x+=1

def getLyrics (url):
    r = requests.get('https://genius.com'+url)
    s = BeautifulSoup(r.text, 'html.parser')

    lyrics = s.find('div', class_='lyrics')
    for p in lyrics('p'):
        lyricsList.append(p.text)

    released = s.find('span', class_='metadata_unit-info metadata_unit-info--text_only')
    try:
        releasedList.append(released.text)
    except:
        releasedList.append('')
    print (url)

for i in page:
    getInfo(i)

rankCounter = 0
for i in linkList:
    getLyrics(i)
    rankCounter +=1
    rankList.append(rankCounter)

with open('raw-output.csv','a', newline='', encoding = 'utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(zip(dateList, songList, rankList, artistList, titleList, viewList, releasedList, linkList, lyricsList))