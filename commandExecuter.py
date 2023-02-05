import random

from datetime import datetime, timedelta
from databaseWrapper import DatabaseWrapper
from messages import *

class CommandExecuter:

    def __init__(self, channel, dbWrapper: DatabaseWrapper):
        self.db = dbWrapper
        self.accountName = self.db.getActiveAccount()
        self.channel = channel
        
    def versus(self, opponent):
        
        [wins, loses] = self.db.getWinsLosesVsOpponent(opponent)
        return versusMsg(self.accountName, wins, loses, opponent)

    def dzisiaj(self):

        todaysDate = datetime.datetime.now().date()
        [wins, loses, pointSum] = self.db.getWinsLosesPointsForDate(todaysDate)

        return todayMsg(self.accountName, wins, loses, pointSum)

    def wczoraj(self):

        yesterdayDate = datetime.datetime.now().date() - timedelta(days = 1)
        [wins, loses, pointSum] = self.db.getWinsLosesPointsForDate(yesterdayDate)

        return yesterdayMsg(self.accountName, wins, loses, pointSum)

    def dzisiaj_detale(self):
        todaysDate = datetime.datetime.now().date()
        results = self.db.getDetailedDate(todaysDate)
        msg = ""
        for enemy_name, [wins, loses] in results.items():
            msg += detailedMatchMsg(enemy_name, wins, loses)
        return msg
    
    def wczoraj_detale(self):
        yesterdayDate = datetime.datetime.now().date() - timedelta(days = 1)
        results = self.db.getDetailedDate(yesterdayDate)
        msg = ""
        for enemy_name, [wins, loses] in results.items():
            msg += detailedMatchMsg(enemy_name, wins, loses)
        return msg
        
    def konto(self, newActiveAccount):
        [points, rating]  = self.db.getPointsAndRank()
        return updateAccountMsg(newActiveAccount, points, rating)

    def punkty(self):
        [points, _]  = self.db.getPointsAndRank()
        return pointsMsg(self.accountName, points)

    def last(self):
        m  = self.db.getLastMatch()
        return lastMatchMsg(m)