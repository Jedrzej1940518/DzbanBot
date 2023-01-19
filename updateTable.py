
import os
import requests
import csv
import json
import datetime
import re
import logging
from bs4 import BeautifulSoup

__maxRangeToGet = 20 
__secondsBetweenUpdates = 300 #5 minutes
__fieldnames = ['endDateTime', 'enemyName', 'hostName', 'durationInSeconds', 'ratingChange']

def __getLastWriteTime():

    with open('internalData.txt', 'r') as file:
        time = file.readline()
        return time

def __updateWriteTime():
    
    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    with open('internalData.txt', 'w') as file:
        file.write(date_time)

def __timePassedBetweenUpdates():
    lastUpdateString = __getLastWriteTime()
    lastUpdateDatetime = datetime.datetime.strptime(lastUpdateString, "%m/%d/%Y, %H:%M:%S")
    now = datetime.datetime.now()
    return now - lastUpdateDatetime

def __getPointsData():

    print(f'getting points')
     
    url = "https://h3score.com/players/profile?name=BiomHammer."
    html = requests.get(url, verify=False).content
    soup = BeautifulSoup(html, 'html.parser')
    
    return soup

def __updatePoints(soup):

    pointTag = soup.find(text = re.compile("Points \d+"))
    points = re.search("\d+", pointTag).group(0)
    
    rankTag = soup.find(text = re.compile("Rank \d+"))
    rank = re.search("\d+", rankTag).group(0)
    
    with open('points.txt', 'w') as f:
        f.write('Points:'+points+'\n')
        f.write('Rank:'+rank+'\n')

def __getMatchData(pageNum, size):

        print(f'getting data: {pageNum}, {size}')
        url = f'https://h3score.com/players/data/lastGameResults?playerName=BiomHammer.&page={pageNum}&size={size}'
        html = requests.get(url, verify=False).content
        data = json.loads(html)
        dataItems = data['data']
        return dataItems


def __getFirstRow():
    
    with open('data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        try:
            return next(reader)
        except StopIteration:
            return False


def __getDataNeeded():

    firstRow = __getFirstRow()
    page = 1
    range = 10
    dataNeeded = []

    while page*range <= __maxRangeToGet:

        data_items = __getMatchData(page, range)

        for item in data_items:
            if __itemInRowCsv(firstRow, item):
                return dataNeeded
            dataNeeded.append(item)

        page +=1

    return dataNeeded


def __mergeTables(neededData):

    with open('new_data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=__fieldnames)
        writer.writeheader()

        for item in neededData:
            writer.writerow(item)

        with open('data.csv', 'r', newline='') as oldFile:
            reader = csv.DictReader(oldFile)
            for row in reader:
                writer.writerow(row)
            
    os.remove('old_data.csv')
    os.rename('data.csv', 'old_data.csv')
    os.rename('new_data.csv', 'data.csv')
 
def __itemInRowCsv(row, item):

    if row['endDateTime'] == item['endDateTime'] and row['enemyName'] == item['enemyName'] and row['hostName'] == item['hostName']:
        return True

    return False

def __createTable():

    numberOfGames = int(input("How many games you want to get? "))
    if numberOfGames > 1000:
        print("error! too many games")
        exit()

    matchData = __getMatchData(1, numberOfGames)

    with open('data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=__fieldnames)

        writer.writeheader()
        for item in matchData:
            writer.writerow(item)

    __updateWriteTime()

def updateTable():
        
    t = __timePassedBetweenUpdates()
    if t.total_seconds() < __secondsBetweenUpdates:
        return 

    __updateWriteTime()

    try:
        neededData = __getDataNeeded()
        soup = __getPointsData()
    except Exception as e:
        logging.error(f'Error while getting data {e}')
        return

    __mergeTables(neededData)
    __updatePoints(soup)
