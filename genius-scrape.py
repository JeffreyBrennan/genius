import requests, csv, time, timing, json
from bs4 import BeautifulSoup

releasedList, linkList, songList, viewList, lyricsList, artistList, titleList, dateList = ([] for i in range(8))
page = [1,2]
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', \
        'August', 'September', 'October', 'November', 'December']
outputPath = 'C:/Users/jeffb/Documents/Python/webPrograms/webScraping/genius/output/genius/'
fileDate = time.strftime('%Y-%m-%d')

checked = time.time()

def getInfo (page):
    r = requests.get('https://genius.com/api/songs/chart?page='+str(page)+'&per_page=50&time_period=day')
    data = json.loads(r.content.decode())

    for i in range(0, 50):
        link = data['response']['chart_items'][i]['item']['path']
        songID = data['response']['chart_items'][i]['item']['id']
        views = data['response']['chart_items'][i]['item']['stats']['pageviews']
        artist = data['response']['chart_items'][i]['item']['primary_artist']['name']       
        title = data['response']['chart_items'][i]['item']['title']

        linkList.append(link)
        songList.append(songID)
        viewList.append(views)
        dateList.append(checked)
        artistList.append (artist)
        titleList.append(title)
        
def getLyrics (url):
    r = requests.get('https://genius.com'+url)
    s = BeautifulSoup(r.text, 'html.parser')

    lyrics = s.find('div', class_='lyrics')
    for p in lyrics('p'):
        lyricsList.append(p.text)

    released = s.find('span', class_='metadata_unit-info metadata_unit-info--text_only')
    try:
        if any(month in released.text for month in months):
            releasedList.append(released.text)
        else:
            releasedList.append('N/A')  
    except:
        releasedList.append('N/A')
    print ('Grabbing lyrics from ' + url)

for i in page:
    getInfo(i)

for i in linkList:
    getLyrics(i)

with open(outputPath+ fileDate + '-genius-top-100.csv','w', newline='', encoding = 'utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(zip(['Time_Checked'], ['Song_ID'], ['Rank'], ['Artist'], \
                        ['Title'], ['Views'], ['Date_Published'], ['Link'], ['Lyrics']))
    writer.writerows(zip(dateList, songList,
                        (i for i in range(1,101)), 
                        artistList, titleList, viewList, releasedList, linkList, lyricsList))