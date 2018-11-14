import requests
import timing
import pandas as pd
from bs4 import BeautifulSoup

# Function to split list into chunks of a given size
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

# Scrapes lyrics from the Genius lyrics page (b/c API doesn't support this for some reason)
def lyric_get(URL):
    try:
        page = requests.get('https://genius.com' + URL)
        html = BeautifulSoup(page.text, 'html.parser')

        lyrics = html.find('div', class_='lyrics').get_text()  # All lyrics from page are included in the 'lyrics' class
        lyrics_list.append(lyrics.strip('\n'))  # Removes '\n' tag from lyrics results but still preserves verse spacing

    except AttributeError:
        lyrics_list.append('N/A')

link_df = pd.read_csv('genius-files/genius-link-ratio.csv')

# Peforms a search on all links that are more than 0.8 similar to their resepective billboard listing
good_links = link_df.loc[link_df['ratio'] > 0.8, 'genius-link'].tolist()
genius_id_list = link_df.loc[link_df['ratio'] > 0.8, 'genius-id'].tolist()

counter = 0
chunklength = 50

# Creates a csv file and writes headers to it
output_df = pd.DataFrame(columns=['genius-id', 'lyrics'])
output_df.to_csv('genius-files/genius-lyrics.csv', mode='w', index=False)

# Splits task into chunks of size (50), writes to csv after each one to perserve data in event of crash / interruption
for chunk in chunker(good_links, chunklength):
    lyrics_list = []  # Creates empty list for new lyrics to be stored into, refreshes every chunk

    for song in chunk:
        lyric_get(song)
        counter += 1
        print(str(counter) + '|' + str(song))  # Outputs number of song and its link to show progress

    # Appends the corresponding genius id and lyrics to a new dataframe which is then outputted
    output_df['genius-id'] = genius_id_list[counter - chunklength: counter]
    output_df['lyrics'] = lyrics_list

    output_df.to_csv('genius-files/genius-lyrics.csv', mode='a', header=False, index=False)
