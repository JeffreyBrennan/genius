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

    df['Combined'] = df['Artist'] + ' ' + df['Title']
    df = df.drop_duplicates(subset='Combined')
    df.to_csv('unique-billboard-songs.csv')
    return df

def title_cleaning(song, artist):
    
    # Song title fixes
    song = song.lower()

    # removes characters between parentheses | removes info after slash
    # tested no significant performance decrease, decided not to include conditional statements
    song = re.sub(r'\(.*\)', '', song)
    song = song.split('/')[0]

    # removes extraneous symbols
    song = song.replace("'", '').replace('...', '').replace('!', '')

    # converts censored expletives to the actual word
    expletives = {'sh*t': 'shit', 's**t': 'shit', 'f*ck': 'fuck', 'f**k': 'fuck', 'f***': 'fuck', 'f*****g': 'fucking', 'f**kin': 'fuckin', 'b*tch': 'bitch', 'b****': 'bitch', 'b***h': 'bitch', 'n****z': 'niggaz', 'n***s': 'niggas', 'ni**as': 'niggas', 'p****': 'pussy', 'a**': 'ass'}

    # ------------ #
    # Artist fixes #
    artist = artist.lower()

    # removes featured artists for cleaner search string
    features = ['Featuring', 'featuring', '&', ',', 'feat', 'feat.', 'Feat.']
    if any(substring in artist for substring in features):
        bool_results = [s in artist for s in features]
        sub_loc = (list(compress(range(len(bool_results)), bool_results)))
        sub = features[sub_loc[0]]
        artist = artist.split(sub, 1)[0]

    # search_list.append(clean_title + ' ' + clean_artist)
    # return search_list

def strcompare(song, link):
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
    title_cleaning(df_unique['Title'][i], df_unique['Artist'][i])

# df_unique['Search term'] = search_list
