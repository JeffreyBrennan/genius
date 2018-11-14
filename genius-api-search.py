import requests
import csv
import time
import timing
import lyricsgenius as genius  # Genius API handler
import pandas as pd

keyGet = open('Key.txt', 'r')  # Reads key from separate file for privacy
API_KEY = keyGet.read()
api = genius.Genius(API_KEY)

# Function to split list into chunks of a given size
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

# Performs search, gets song id and web link for first song
def link_get(query):
    try:
        data = api.search_genius(query)
        song_id.append(data['hits'][0]['result']['id'])
        genius_link.append(data['hits'][0]['result']['path'])

    except IndexError:
        song_id.append('N/A')
        genius_link.append('N/A')

# Grabs search terms from csv and saves as a list
input_path = r'genius-files\genius-search-terms.csv'
search_df = pd.read_csv(input_path)
search_list = search_df['Search term']

# Creates a csv file and writes headers to it
output_df = pd.DataFrame(columns=['genius-id', 'genius-link'])
output_df.to_csv('genius-files/genius-results.csv', mode='a', index=False)

counter = 0
# Splits task into chunks of size (50), writes to csv after each one to perserve data in event of crash / interruption
for chunk in chunker(search_list, 50):
    song_id = []
    genius_link = []

    for song in chunk:
        link_get(song)
        counter += 1
        print(str(counter) + '|' + str(song))

    # Appends the corresponding genius id and link to a new dataframe which is then outputted
    output_df['genius-id'] = song_id
    output_df['genius-link'] = genius_link

    output_df.to_csv('genius-files/genius-results.csv', mode='a', header=False, index=False)
