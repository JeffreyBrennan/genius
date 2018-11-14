import difflib
import timing
import pandas as pd
import re
from itertools import compress

# initialize lists to be used in song cleaning
ratio_list = []
search_list = []
clean_links = []

# Drops duplicate songs from the og dataset based on their combined artist - title
def bb_unique_songs(df):
    df.drop_duplicates(subset='Combined', inplace=True)
    df.index.names = ['chart-id']  # Keeps index position showing where it used to be located in chart

    # Creates new index to access each of the unique songs, named ('unique-id')
    df = df.reset_index()
    df.index.names = ['unique-id']

    df.to_csv('billboard-files/unique-billboard-songs.csv')  # outputs to csv to save for later usage
    return df

# Replaces censored billboard titles of songs with their respective expletive (to obtain full lyrics from Genius)
def bb_censor_replacer(title, censor_dict):
    for item in censor_dict.keys():
        if item in title:
            title = title.replace(item, censor_dict[item])

    return title

# Cleans titles of billboard songs to create a better search term for the Genius API
def bb_title_cleaner(song):
    song = song.lower()

    # removes characters between parentheses | removes info after slash
    # tested no significant performance decrease, decided not to include conditional statements
    song = re.sub(r'\(.*\)', '', song)
    song = song.split('/')[0]

    # removes extraneous symbols
    song = song.replace("'", '').replace('...', '').replace('!', '')

    # converts censored expletives (csv -> dictionary) to the actual word
    expletives = pd.read_csv('helper-files/expletives.csv', index_col='censored').to_dict()['uncensored']
    song = bb_censor_replacer(song, expletives)

    # removes whitespace from the text
    song = song.strip()

    return song

# Cleans artists of billboard songs to create a better search term for the Genius API
def bb_artist_cleaner(artist):
    artist = artist.lower()

    # List of common feature indicators to be removed to improve search accuracy and shorten search term
    features = ['featuring', '&', ',', 'feat', 'feat.', 'With']

    if any(substring in artist for substring in features):
        bool_results = [s in artist for s in features]
        sub_loc = (list(compress(range(len(bool_results)), bool_results)))

        # For each feature term found in features list, split artist and get the left part
        for i in range(len(sub_loc)):
            sub = features[sub_loc[i]]
            artist = artist.split(sub, 1)[0]

    # Removes whitespace and replaces common extraneous symbols found in artist names
    artist = artist.replace('*', '')
    artist = artist.strip()

    return artist

# Parent function that separately obtains cleaned titles and artists and appends them to a search list
def bb_search_cleaner(song, artist):
    # Calls separate title and artist functions to clean the resulting search term
    clean_title = bb_title_cleaner(song)
    clean_artist = bb_artist_cleaner(artist)

    search_list.append(clean_artist + ' ' + clean_title)

# Parent function that iteratively cleans each artist-title combo and outputs final result to a csv
def bb_search_converter():
    df = pd.read_csv('billboard-files/billboard-songs.csv', encoding='ISO-8859-1', low_memory=False)
    df_unique = bb_unique_songs(df)

    for i in range(len(df_unique)):
        bb_search_cleaner(df_unique['Title'][i], df_unique['Artist'][i])
        print(i)
    df_unique['Search term'] = search_list

    df_unique.to_csv('genius-files/genius-search-terms.csv')

# Cleans links that are returned from the Genius API call
def genius_link_cleaner(link):
    link = link.lower()
    link = link.replace('-', ' ').replace('lyrics', '').replace('/', '')

    link = link.strip()

    clean_links.append(link)

# Parent function that iteratively cleans links returned from Genius API call and outputs result to csv
def genius_result_converter():
    genius_df = pd.read_csv('genius-files/genius-results.csv')

    for i in range(len(genius_df)):
        genius_link_cleaner(str(genius_df['genius-link'][i]))
        print(i)
    genius_df['Cleaned link'] = clean_links

    genius_df.to_csv('genius-files/genius-cleaned-links.csv')

# Creates a ratio of similarity between the search term and the returned link
def analysis_ratio(song, link):
    ratio = difflib.SequenceMatcher(None, song, link).ratio()
    ratio_list.append(round(ratio, 3))

# Parent function that iteratively creates similarity ratios for genius links and search terms and outputs to csv
def analysis_str_compare():
    clean_link_df = pd.read_csv('genius-files/genius-cleaned-links.csv')
    search_df = pd.read_csv('genius-files//genius-search-terms.csv')

    analysis_df = pd.merge(search_df, clean_link_df, left_index=True, right_index=True)
    analysis_df.drop(['Unnamed: 0'], axis=1, inplace=True)  # Drops leftover index column from the genius link csv

    # Converts search terms and links to strings to avoid cases where the song name is a number etc
    for i in range(len(analysis_df)):
        analysis_ratio(str(analysis_df['Search term'][i]), str(analysis_df['Cleaned link'][i]))
        print(i)

    analysis_df['ratio'] = ratio_list

    analysis_df.to_csv('genius-files/genius-link-ratio.csv', encoding='ISO-8859-1', index=False)

# Call the required function
# bb_search_converter()
# genius_link_converter()
# analysis_str_compare()
