import csv
import random
import re
from datetime import datetime, timedelta

earliestRecording = datetime.strptime("1/17/2023", "%m/%d/%Y")
dateFormat = "%Y-%m-%dT%H:%M:%SZ"
todaySeconds = 43200 #12 godzin

def __won(row) -> bool:
    
    if int(row['ratingChange']) > 0:
        return True

    return False

def __points(row):
    return int(row['ratingChange'])

def __getWinsLosePoints(rows):

    wins = 0
    loses = 0
    pointSum = 0

    for row in rows:

        pointSum += __points(row)

        if __won(row):
            wins+=1
        else:
            loses+=1

    return (wins, loses, pointSum)
    

def __getRows(earliestDate, latestDate):
    
    rowList = []

    with open('data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            timestamp = datetime.strptime(row['endDateTime'], "%Y-%m-%dT%H:%M:%SZ")
            
            if timestamp < earliestDate or timestamp > latestDate:
                return rowList
            if timestamp > earliestDate and timestamp < latestDate:
                rowList.append(row)
    
    return rowList


def versus(opponent):

    rows = __getRows(earliestRecording, datetime.now())
    rowsVersus = [row for row in rows if row['enemyName'].casefold() == opponent.casefold()]
    
    [wins, loses, ] =__getWinsLosePoints(rowsVersus)

    return (wins, loses)

def dzisiaj():
    
    
    earliestDate = datetime.now() - timedelta(seconds=todaySeconds)
    rows = __getRows(earliestDate, datetime.now())
    
    [wins, loses, pointSum] = __getWinsLosePoints(rows)
    
    return (wins, loses, pointSum)

def getRating():

    with open('points.txt', 'r') as f:
        pointsLine = f.readline()
        points = re.search('(Points:)(\d+)', pointsLine).group(2)
        rankLine = f.readline()
        rank = re.search('(Rank:)(\d+)', rankLine).group(2)
        return (points, rank)

    pass

def negativeEmote():
    negativeEmotes = ['classic', 'Pain', 'depresso', 'xddinside', 'xddWalk', 'PepeHands', 'AYAYAS']
    return random.choice(negativeEmotes)

def positiveEmote():
    positiveEmotes = ['leosiaKiss', 'fifka', 'leosiaJAM', 'pajac', 'AYAYASmile', 'WICKED', 'PagMan']
    return random.choice(positiveEmotes)

def neutralEmote():
    neutralEmotes = ['HUH', 'hmjj']
    return random.choice(neutralEmotes)

def emotePoints(points):
    if points > 0:
        return positiveEmote()
    elif points < 0:
        return negativeEmote()
    else:
        return neutralEmote()
    
def emoteWins(wins, loses):
    if wins > loses:
        return positiveEmote()
    elif loses > wins:
        return negativeEmote()
    else:
        return neutralEmote()