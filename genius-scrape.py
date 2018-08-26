import requests, time, timing, json, pandas
from bs4 import BeautifulSoup

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', \
        'August', 'September', 'October', 'November', 'December']

header = ['Song_ID', 'Time_Checked', 'Artist', 'Title', 'Views', 'Link', 'Date_Published', 'Lyrics']


outputPath = 'C:/Users/jeffb/Documents/Python/webPrograms/webScraping/genius/output/genius-songs/'
fileDate = time.strftime('%Y-%m-%d')
date = time.time()

results = {}

def getSongInfo ():
    for page in range(1, 3):
        rank = (50 * page) - 49 ## (enables 1-100 rank w/ 50 results per page)
        r = requests.get('https://genius.com/api/songs/chart?page='+str(page)+'&per_page=50&time_period=day')
        data = json.loads(r.content.decode())
        for i in range(0, 50): ## (i=0 -> i=49 | corresponds to list positions for items 1,50)
            link = data['response']['chart_items'][i]['item']['path']
            song = data['response']['chart_items'][i]['item']['id']
            views = data['response']['chart_items'][i]['item']['stats']['pageviews']
            artist = data['response']['chart_items'][i]['item']['primary_artist']['name']       
            title = data['response']['chart_items'][i]['item']['title']

            results[rank] = [song, date, artist, title, views, link]
            rank += 1

def getLyrics (i):
    url = results[i][5]
    r = requests.get('https://genius.com'+url)
    soup = BeautifulSoup(r.text, 'html.parser')

    released = soup.find('span', class_='metadata_unit-info metadata_unit-info--text_only')
    try:
        if any(month in released.text for month in months):
            results[i].append(released.text)
        else:
            results[i].append('N/A')  
    except:
        results[i].append('N/A')

    lyrics = soup.find('div', class_='lyrics')
    
    for lyric in lyrics('p'):pass
    if lyric: 
        results[i].append(lyric.text)
        

    print ('(' + str(i) + ') Grabbing lyrics from ' + url)

getSongInfo()

for i in results:
    getLyrics(i)

df = pandas.DataFrame(results).T
df.columns = header
df.to_csv(outputPath + fileDate + '-genius-top-100.csv')