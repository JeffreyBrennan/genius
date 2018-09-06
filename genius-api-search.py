import requests, csv, time, timing, json, os
import lyricsgenius as genius
import pandas as pd

searchList = []
songid = []
geniuslink = []
geniusidlist = []

linkpath = 'C:/Users/jeffb/Documents/Python/webPrograms/webScraping/lyrics/linkmatch-cleanup.csv'
lyricpath = 'C:/Users/jeffb/Documents/Python/webPrograms/webScraping/lyrics/genius-lyric-search.csv'

keyGet = open('Key.txt', 'r')
API_KEY = keyGet.read()
api = genius.Genius(API_KEY)


with open(linkpath, newline='') as r:
        file = csv.reader(r, delimiter =',')
        for row in file:
            for i in row:
                searchList.append(i)

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def linkget(query):

    try:
        data = api.search_genius(query)
        songid.append(data['hits'][0]['result']['id'])
        geniuslink.append(data['hits'][0]['result']['path'])

    except:
        songid.append('N/A')
        geniuslink.append('N/A')


counter = 0
for chunk in chunker(searchList, 100):
    
    songid = []
    geniuslink = []

    for song in chunk:
            linkget(song)
            counter +=1
            print (str(counter) + '|' + str(song))

    with open('genius-searchlist-links-2.csv','a', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(zip(songid, geniuslink))
