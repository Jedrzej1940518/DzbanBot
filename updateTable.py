
import os
import requests
import csv
import json
import datetime

maxRangeToGet = 20 
secondsBetweenUpdates = 600

fieldnames = ['endDateTime', 'enemyName', 'hostName', 'durationInSeconds', 'ratingChange']

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

def __getData(pageNum, size):

        print(f'getting data: {pageNum}, {size}')
        url = f'https://h3score.com/players/data/lastGameResults?playerName=BiomHammer.&page={pageNum}&size={size}'
        html = requests.get(url, verify=False).content
        data = json.loads(html)
        dataItems = data['data']
        return dataItems


def __createTable():

    numberOfGames = int(input("How many games you want to get? "))
    if numberOfGames > 1000:
        print("error! too many games")
        exit()

    data_items = __getData(1, numberOfGames)

    with open('data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for item in data_items:
            writer.writerow(item)

    __updateWriteTime()

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

    while page*range <= maxRangeToGet:

        data_items = __getData(page, range)

        for item in data_items:
            if itemInRowCsv(firstRow, item):
                return dataNeeded
            dataNeeded.append(item)

        page +=1

    return dataNeeded


def mergeTables():

    data_items = __getDataNeeded()

    with open('new_data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for item in data_items:
            writer.writerow(item)

        with open('data.csv', 'r', newline='') as oldFile:
            reader = csv.DictReader(oldFile)
            for row in reader:
                writer.writerow(row)
            
    os.remove('old_data.csv')
    os.rename('data.csv', 'old_data.csv')
    os.rename('new_data.csv', 'data.csv')


 
def itemInRowCsv(row, item):

    if row['endDateTime'] == item['endDateTime'] and row['enemyName'] == item['enemyName'] and row['hostName'] == item['hostName']:
        return True

    return False



def updateTable():
        
    t = __timePassedBetweenUpdates()
    if t.total_seconds() < secondsBetweenUpdates:
        return 
    
    mergeTables()
    __updateWriteTime()