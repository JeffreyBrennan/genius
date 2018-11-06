import difflib
import timing
import pandas as pd
import re
from itertools import compress

ratiolist = []
songlist = []
linklist = []
search_list = []

def unique_get(df):
    # Creates combined column (assuming it does not exist and removes duplicate values)
    # df['Combined'] = df['Artist'] + ' ' + df['Title']
    df = df.drop_duplicates(subset='Combined')
    df.to_csv('unique-billboard-songs.csv')
    return df

def censor_replace(title, censor_dict):
    for item in dict.keys():
        if item in title:
            title = title.replace(item, censor_dict[item])

    return title

def title_cleaner(song):
    # ----------Song title fixes---------- #
    song = song.lower()

    # removes characters between parentheses | removes info after slash
    # tested no significant performance decrease, decided not to include conditional statements
    song = re.sub(r'\(.*\)', '', song)
    song = song.split('/')[0]

    # removes extraneous symbols
    song = song.replace("'", '').replace('...', '').replace('!', '')

    # converts censored expletives (csv -> dictionary) to the actual word
    expletives = pd.read_csv('expletives.csv', index_col='censored').to_dict()['uncensored']
    song = censor_replace(song, expletives)

    return song

def artist_cleaner(artist):
    artist = artist.lower()

    # removes featured artists for cleaner search string
    features = ['Featuring', 'featuring', '&', ',', 'feat', 'feat.', 'Feat.']
    
    if any(substring in artist for substring in features):
        bool_results = [s in artist for s in features]
        sub_loc = (list(compress(range(len(bool_results)), bool_results)))
        sub = features[sub_loc[0]]
        artist = artist.split(sub, 1)[0]

    return artist

def search_clean(song, artist):
    # Calls separate title and artist functions to clean the resulting search term
    clean_title = title_cleaner(song)
    clean_artist = artist_cleaner(artist)

    search_list.append(clean_title + ' ' + clean_artist)
    
def str_compare(song, link):
    ratio = difflib.SequenceMatcher(None, song, link).ratio()
    ratiolist.append(ratio)
    print(len(ratiolist))

# for i in range(len(df)):
#     strcompare(df['song'][i], df['split-link'][i])

# df['ratio'] = ratiolist

# df.to_csv('genius-link-ratio-2.csv', encoding='ISO-8859-1')

df = pd.read_csv('billboard-songs.csv', encoding='ISO-8859-1', low_memory=False)
df_unique = unique_get(df)

for i in range(len(df_unique)):
    search_clean(df_unique['Title'][i], df_unique['Artist'][i])

# df_unique['Search term'] = search_list
