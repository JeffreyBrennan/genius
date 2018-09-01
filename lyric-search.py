import requests, csv, time, timing, json
from bs4 import BeautifulSoup

path = 'C:/Users/jeffb/Documents/Python/webPrograms/webScraping/genius/output/billboard-songs/'

searchList = []

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


with open(path+'searchlist.csv', newline='') as r:
        file = csv.reader(r, delimiter =',')
        for row in file:
            for i in row:
                searchList.append(i)
counter = 0
for chunk in chunker(searchList, 1000):
    resultlist = []
    for song in chunk:
        try: 
            r = requests.get('https://search.azlyrics.com/search.php?q=' + song)
            s = BeautifulSoup(r.text, 'html.parser')

            test = s.find('td', class_='text-left visitedlyr')
            for link in test('a'):
                    if link.has_attr('href'):
                        resultlist.append(link['href'])
                        counter +=1
                        print (str(counter) + '| success')
        except:
            resultlist.append('N/A')
            counter +=1
            print (str(counter) + '| fail')

                    
    with open(path+'links.csv','a', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(zip(resultlist))