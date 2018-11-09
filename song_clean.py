import difflib
import timing
import pandas as pd
import re
from itertools import compress

ratio_list = []
search_list = []
clean_links = []

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
    ratio_list.append(ratio)
    print(len(ratio_list))

def search_analysis():
    link_df = pd.read_csv('cleaned-links.csv')
    song_df = pd.read_csv('csv-files/genius-search-terms.csv')

    # analysis_df = link_df + song_df
    analysis_df = pd.merge(song_df, link_df[['genius-id', 'link']], on='unique-id')

    for i in range(len(analysis_df)):
        str_compare(analysis_df['Search term'][i], analysis_df['Link'][i])

    analysis_df['ratio'] = ratio_list

    analysis_df.to_csv('genius-link-ratio', encoding='ISO-8859-1')

def song_clean():
    df = pd.read_csv('billboard-songs.csv', encoding='ISO-8859-1', low_memory=False)
    df_unique = unique_get(df)

    for i in range(len(df_unique)):
        search_clean(df_unique['Title'][i], df_unique['Artist'][i])
        print(i)
    df_unique['Search term'] = search_list

    df_unique.to_csv('genius-search-terms.csv')

def genius_cleaner(link):
    link = link.lower()

    link = link.replace('-', ' ').replace('lyrics', '')

    clean_links.append(link)

def link_clean():
    link_df = pd.read_csv('genius-results.csv', encoding='ISO-8859-1', low_memory=False)

    for i in range(len(link_df)):
        genius_cleaner(link_df['Link'])

    link_df.to_csv('cleaned_links.csv')

# song_clean()
link_clean()
# search_analysis()
