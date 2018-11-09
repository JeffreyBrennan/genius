import requests
import csv
import time
import timing
import lyricsgenius as genius
import pandas as pd

searchList = []
songid = []
geniuslink = []
geniusidlist = []

input_path = r'csv-files\genius-search-terms.csv'

keyGet = open('Key.txt', 'r')
API_KEY = keyGet.read()
api = genius.Genius(API_KEY)

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def link_get(query):
    try:
        data = api.search_genius(query)
        song_id.append(data['hits'][0]['result']['id'])
        genius_link.append(data['hits'][0]['result']['path'])

    except IndexError:
        song_id.append('N/A')
        genius_link.append('N/A')

search_df = pd.read_csv(input_path)
search_list = search_df['Search term']

counter = 0
output_df = pd.DataFrame(columns=['genius-id', 'genius-link'])
output_df.to_csv('genius-results.csv', mode='a', index=False)

for chunk in chunker(search_list, 10):
    song_id = []
    genius_link = []

    for song in chunk:
        link_get(song)
        counter += 1
        print(str(counter) + '|' + str(song))

    output_df['genius-id'] = song_id
    output_df['genius-link'] = genius_link

    output_df.to_csv('genius-results.csv', mode='a', header=False, index=False)
