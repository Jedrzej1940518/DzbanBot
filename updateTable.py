
import os
import requests
import csv
import json
import datetime
import re
import logging
from bs4 import BeautifulSoup

dateFormat = "%Y-%m-%dT%H:%M:%SZ"

fieldnames = ['endDateTime', 'enemyName',
              'hostName', 'durationInSeconds', 'ratingChange']

__maxRangeToGet = 20
__secondsBetweenUpdates = 300  # 5 minutes


def __updateInternalData(fieldName, newValue):

    with open('internalData.json', 'r') as file:
        data = json.load(file)

    data[fieldName] = newValue

    with open('internalData.json', 'w') as file:
        json.dump(data, file)


def __getLastWriteTime():

    with open('internalData.json', 'r') as file:
        data = json.load(file)
        return data["LastUpdate"]


def __updateWriteTime():

    now = datetime.datetime.now()
    updateTime = now.strftime(dateFormat)

    __updateInternalData("LastUpdate", updateTime)


def __timePassedBetweenUpdates():
    lastUpdateString = __getLastWriteTime()
    lastUpdateDatetime = datetime.datetime.strptime(
        lastUpdateString, dateFormat)

    now = datetime.datetime.now()
    return now - lastUpdateDatetime


def __getPointsData():

    logging.info(f'getting points')

    url = "https://h3score.com/players/profile?name=BiomHammer."
    html = requests.get(url, verify=False).content
    soup = BeautifulSoup(html, 'html.parser')

    return soup


def __updatePoints(soup):

    pointTag = soup.find(text=re.compile("Points \d+"))
    points = re.search("\d+", pointTag).group(0)

    __updateInternalData("Points", points)

    rankTag = soup.find(text=re.compile("Rank \d+"))
    rank = re.search("\d+", rankTag).group(0)

    __updateInternalData("Rank", rank)


def __getMatchData(pageNum, size):

    logging.info(f'getting data: {pageNum}, {size}')
    url = f'https://h3score.com/players/data/lastGameResults?playerName=BiomHammer.&page={pageNum}&size={size}'
    html = requests.get(url, verify=False).content
    data = json.loads(html)
    dataItems = data['data']
    return dataItems


def __getFirstRow():

    with open('data.json', 'r') as file:
        reader = csv.DictReader(csvfile)

        try:
            return next(reader)
        except StopIteration:
            return False


def __getDataNeeded():

    lastMatch = __getLastMatch()
    page = 1
    range = 10
    dataNeeded = []

    while page*range <= __maxRangeToGet:

        data_items = __getMatchData(page, range)

        for item in data_items:
            if __itemInRowCsv(firstRow, item):
                return dataNeeded
            dataNeeded.append(item)

        page += 1

    return dataNeeded


def __mergeTables(neededData):

    with open('new_data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
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
        logging.info("error! too many games")
        exit()

    matchData = __getMatchData(1, numberOfGames)

    with open('data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

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


def jsonTesting():


    with open('jsonTest.json', 'r') as file:
        data = json.load(file)
    
    for record in data:
        print(record)

    
    with open("jsonTest.json", "r") as file:
        first_line = file.readline()
        print(first_line)


jsonTesting()