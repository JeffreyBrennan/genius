import difflib
import timing
import pandas as pd
import re
from itertools import compress

ratiolist = []
search_list = []

def unique_get(df):
    df.drop_duplicates(subset='Combined', inplace=True)
    df.index.names = ['chart-id']
    df = df.reset_index()
    df.index.names = ['unique-id']

    df.to_csv('unique-billboard-songs.csv')
    return df

def censor_replace(title, censor_dict):
    for item in censor_dict.keys():
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

    song = song.strip()

    return song

def artist_cleaner(artist):
    artist = artist.lower()

    # removes featured artists for cleaner search string
    features = ['featuring', '&', ',', 'feat', 'feat.']

    if any(substring in artist for substring in features):
        bool_results = [s in artist for s in features]
        sub_loc = (list(compress(range(len(bool_results)), bool_results)))
        sub = features[sub_loc[0]]
        artist = artist.split(sub, 1)[0]
    artist = artist.strip()

    return artist

def search_clean(song, artist):
    # Calls separate title and artist functions to clean the resulting search term
    clean_title = title_cleaner(song)
    clean_artist = artist_cleaner(artist)

    search_list.append(clean_artist + ' ' + clean_title)

def str_compare(song, link):
    ratio = difflib.SequenceMatcher(None, song, link).ratio()
    ratiolist.append(ratio)
    print(len(ratiolist))

def search_analysis():
    df = pd.read_csv('genius-results')
    for i in range(len(df)):
        str_compare(df['song'][i], df['split-link'][i])

    df['ratio'] = ratiolist

    df.to_csv('genius-link-ratio-2.csv', encoding='ISO-8859-1')

def initial_clean():
    df = pd.read_csv('billboard-songs.csv', encoding='ISO-8859-1', low_memory=False)
    df_unique = unique_get(df)

    for i in range(len(df_unique)):
        search_clean(df_unique['Title'][i], df_unique['Artist'][i])
        print(i)
    df_unique['Search term'] = search_list

    df_unique.to_csv('genius-search-terms.csv')

initial_clean()