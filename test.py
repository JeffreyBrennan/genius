import requests, csv, time, timing, json
from bs4 import BeautifulSoup


r = requests.get('https://genius.com/Drake-in-my-feelings-lyrics')
s = BeautifulSoup(r.text, 'html.parser')


released = s.find('span', class_='metadata_unit-info metadata_unit-info--text_only')

print (lyrics.text)