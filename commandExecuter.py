import random

from datetime import datetime, timedelta
import databaseWrapper
from messages import *

class CommandExecuter:

    def __init__(self, channel, dbWrapper):
        self.db = dbWrapper
        self.accountName = self.db.getActiveAccount()
        self.channel = channel
        
    def versus(self, opponent):
        
        [wins, loses] = self.db.getWinsLosesVsOpponent(opponent)
        return versusMsg(self.accountName, wins, loses, opponent)

    def dzisiaj(self):

        todaysDate = datetime.now().date()
        [wins, loses, pointSum] = self.db.getWinsLosesPointsForDate(todaysDate)

        return todayMsg(self.accountName, wins, loses, pointSum)

    def wczoraj(self):

        yesterdayDate = datetime.now().date() - timedelta(days = 1)
        [wins, loses, pointSum] = self.db.getWinsLosesPointsForDate(yesterdayDate)

        return yesterdayMsg(self.accountName, wins, loses, pointSum)

    def konto(self, newActiveAccount):
        [points, rating]  = self.db.getPointsAndRank()
        return updateAccountMsg(newActiveAccount, points, rating)

    def punkty(self):
        [points, _]  = self.db.getPointsAndRank()
        return pointsMsg(self.accountName, points)
