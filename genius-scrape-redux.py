import requests, time, timing, json, pandas, csv
from bs4 import BeautifulSoup

geniusidlist = []
linklist = []
idlist = []

lyricpath = 'C:/Users/jeffb/Documents/Python/webPrograms/webScraping/lyrics/genius-lyric-search.csv'

with open(lyricpath, newline='') as r:
        reader = csv.reader(r, delimiter =',')
        for row in reader:
            idlist.append(row[0])
            linklist.append(row[1])

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def lyricget (URL):
        
    try:
        page = requests.get("https://genius.com" + URL)
        html = BeautifulSoup(page.text, "html.parser")

        lyrics = html.find("div", class_="lyrics").get_text()
        lyricslist.append(lyrics.strip('\n'))
    except:
        lyricslist.append('N/A')

counter = 0
chunklength = 50
for chunk in chunker(linklist, chunklength):
    lyricslist = []

    for song in chunk:

            lyricget(song)
            counter +=1
            print (str(counter) + '|' + str(song))
    try:
        with open('genius-all-billboard-lyrics.csv','a', newline='', encoding='UTF-8') as f:
                    writer = csv.writer(f)
                    writer.writerows(zip(idlist[counter-chunklength:counter], lyricslist))
    except:
        continue