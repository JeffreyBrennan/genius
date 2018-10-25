import requests
import time
import timing
import pandas
import datetime
import csv
from bs4 import BeautifulSoup

def getSaturdays():
    getdate = datetime.datetime.now()
    getday = datetime.datetime.now().weekday()
    datefix = (getdate + datetime.timedelta(days=5 - getday)).date()

    startdate = datefix.strftime('%Y-%m-%d')
    enddate = '1961-12-25'

    currentday = datetime.datetime.strptime(startdate, '%Y-%m-%d').date()

    d2 = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    d1 = datetime.datetime.strptime(enddate, '%Y-%m-%d')
    delta = d2 - d1
    weekCount = delta.days // 7

    with open('datelist.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for i in range(1, weekCount):
            dayint = i * 7
            week = (currentday - datetime.timedelta(days=dayint))
            writer.writerow([week])
def getMondays():
    startdate = '1958-08-04'
    enddate = '1961-12-25'

    cleanend = datetime.datetime.strptime(enddate, '%Y-%m-%d').date()

    d1 = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(enddate, '%Y-%m-%d')
    delta = d2 - d1
    weekCount = delta.days // 7

    with open('datelist.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        for i in range(1, weekCount):
            dayint = i * 7
            week = (cleanend - datetime.timedelta(days=dayint))
            writer.writerow([week])

getMondays()
