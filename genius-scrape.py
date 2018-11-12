import requests
import time
import timing
import json
import pandas as pd
import csv
from bs4 import BeautifulSoup

link_path = ('genius-link-ratio.csv')

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def lyric_get(URL):
    try:
        page = requests.get("https://genius.com" + URL)
        html = BeautifulSoup(page.text, "html.parser")

        lyrics = html.find("div", class_="lyrics").get_text()
        lyrics_list.append(lyrics.strip('\n'))

    except AttributeError:
        lyrics_list.append('N/A')

link_df = pd.read_csv(link_path)
all_links = link_df['genius-link']
good_links = link_df.loc[link_df['ratio'] > 0.8, 'genius-link'].tolist()
genius_id_list = link_df['genius-id']

counter = 0
chunklength = 50

# for chunk in chunker(good_links, chunklength):

lyrics_list = []

for song in good_links:
    lyric_get(song)
    counter += 1
    print(str(counter) + '|' + str(song))


output_df = pd.DataFrame(columns=['genius-id', 'lyrics'])
output_df.to_csv('genius-lyrics.csv', mode='a', index=False)

output_df['genius-id'] = genius_id_list
output_df['lyrics'] = lyrics_list
link_df.to_csv('genius-lyrics.csv', mode='a', header=False, index=False)
