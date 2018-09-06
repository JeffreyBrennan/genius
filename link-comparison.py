import difflib, timing, pandas as pd
ratiolist = []
songlist = []
linklist = []

path = 'C:/Users/jeffb/Documents/Python/webPrograms/webScraping/lyrics/genius-lyricmatch-2.csv'

df = pd.read_csv(path, encoding='ISO-8859-1')

def strcompare (song, link):
    ratio = difflib.SequenceMatcher(None, song, link).ratio()
    ratiolist.append(ratio)
    print (len(ratiolist))

for i in range(len(df)):
    strcompare(df['song'][i], df['split-link'][i])

df['ratio'] = ratiolist


df.to_csv('genius-link-ratio-2.csv', encoding='ISO-8859-1')