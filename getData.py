import csv
import random
from datetime import datetime

last_date = datetime.strptime("1/17/2023", "%m/%d/%Y")
today_seconds = 36000

def __won(row) -> bool:
    
    if int(row['ratingChange']) > 0:
        return True

    return False

def __points(row):
    return int(row['ratingChange'])

def versus(opponent, withTime: bool):

    wins = 0
    loses = 0
    # Open the CSV file
    with open('data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        # Loop over the rows in the CSV file
        for row in reader:

            timestamp = datetime.strptime(row['endDateTime'], "%Y-%m-%dT%H:%M:%SZ")
            
            if withTime and timestamp < last_date:
                return (wins, loses)

            if row['enemyName'].casefold() == opponent.casefold():
                if __won(row):
                    wins += 1
                else:
                    loses +=1

    return (wins, loses)

def dzisiaj():
    
    wins = 0 
    loses = 0
    pointSum = 0

    with open('data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        now = datetime.now()
        
        for row in reader:
            timestamp = datetime.strptime(row['endDateTime'], "%Y-%m-%dT%H:%M:%SZ")
            diff = now - timestamp 

            if diff.total_seconds() < today_seconds: #10 hours
                
                pointSum += __points(row)

                if __won(row):
                    wins+=1
                else:
                    loses+=1
            else:
                return (wins, loses, pointSum)
    
    return (wins, loses, pointSum)


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