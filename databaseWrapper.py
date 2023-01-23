

import MySQLdb
import datetime
from collections import defaultdict

# Internal data:
# channel   active_account  points  rank    last_update

# Match_History:
# account_name  end_date_time   end_date    enemy_name  host_name   duration_in_seconds rating_change

# match fieldnames = ['endDateTime', 'enemyName',
#                      'hostName', 'durationInSeconds', 'ratingChange']


class MatchHistoryObject:

    def __init__(self, row):
        self.account_name = row[0]
        self.end_date_time = row[1]
        self.end_date = row[2]
        self.enemy_name = row[3]
        self.host_name = row[4]
        self.duration_in_seconds = row[5]
        self.rating_change = row[6]

class DatabaseWrapper:

    def __init__(self, channelName):

        self.db = MySQLdb.connect(host="Jedrzej.mysql.pythonanywhere-services.com",
                                  user="Jedrzej", password="7K7FvNy3b_fsAk@", database="Jedrzej$DzbanBot")
        self.c = self.db.cursor()
        self.channelName = channelName
        pass

    def __query(self, query, values):

        self.c.execute(query, values)
        self.db.commit()

    def __fetchOne(self, query, values):

        self.c.execute(query, values)
        return self.c.fetchone()[0]

    def __getDbValuesFromMatch(self, match, activeAccount):

        dateFormat = "%Y-%m-%dT%H:%M:%SZ"
        endDateTime = match['endDateTime']
        endDate = datetime.datetime.strptime(endDateTime, dateFormat).date()

        return (activeAccount, endDateTime, str(endDate), match['enemyName'], match['hostName'],
                match['durationInSeconds'], match['ratingChange'])

    def __matchRecorded(self, match):

        activeAccount = self.getActiveAccount()
        endDateTime = match['endDateTime']
        enemyName = match['enemyName']

        matches = self.c.execute("""SELECT * FROM Match_History WHERE account_name = %s AND end_date_time = %s AND enemy_name = %s""",
                                 (activeAccount, endDateTime, enemyName))
        self.c.fetchone()

        return self.c.rowcount > 0

    def updateWriteTime(self, datetime):

        self.__query("""UPDATE Internal_Data SET last_update = %s WHERE channel = %s""",
                     (datetime, self.channelName))

    def updateRating(self, points, rank):

        self.__query("""UPDATE Internal_Data 
                  SET points = %s, rank = %s
                  WHERE channel = %s""",
                     (points, rank, self.channelName))

    def updateActiveAccount(self, newActiveAccount):
        self.__query("""UPDATE Internal_Data SET active_account = %s WHERE channel = %s""",
                     (newActiveAccount, self.channelName))

    def addMatchIfNotExist(self, match, activeAccount):

        matchAdded = True

        if self.__matchRecorded(match):
            return not matchAdded

        query = ("""INSERT INTO Match_History\
                     (account_name, end_date_time, end_date, enemy_name, host_name, duration_in_seconds, rating_change)\
                     VALUES (%s, %s, %s, %s, %s, %s, %s)""")

        values = self.__getDbValuesFromMatch(match, activeAccount)
        self.__query(query, values)

        return matchAdded

    def getActiveAccount(self):
        return self.__fetchOne("""SELECT active_account FROM Internal_Data WHERE channel = %s""", (self.channelName,))

    def getLastUpdateTime(self):

        return self.__fetchOne(
            """SELECT last_update FROM Internal_Data WHERE channel = %s""", (self.channelName,))

    def getWinsLosesVsOpponent(self, enemyName):

        acc = self.getActiveAccount()
        wins = self.__fetchOne(
            """SELECT COUNT(*) FROM Match_History WHERE account_name = %s AND enemy_name = %s AND rating_change>0""", (acc, enemyName,))

        loses = self.__fetchOne(
            """SELECT COUNT(*) FROM Match_History WHERE account_name = %s AND enemy_name = %s AND rating_change<0""", (acc, enemyName,))

        return (wins or 0, loses or 0)

    def getWinsLosesPointsForDate(self, date):  # TODO REFACTOR THIS

        acc = self.getActiveAccount()

        wins = self.__fetchOne(
            """SELECT COUNT(*) FROM Match_History WHERE account_name = %s AND end_date = %s AND rating_change>0""", (acc, date,))

        loses = self.__fetchOne(
            """SELECT COUNT(*) FROM Match_History WHERE account_name = %s AND end_date = %s AND rating_change<0""", (acc, date,))

        points = self.__fetchOne(
            """SELECT SUM(rating_change) FROM Match_History WHERE account_name = %s AND end_date = %s""", (acc, date,))

        return (wins or 0, loses or 0, points or 0)
    
    def getDetailedDate(self, date):
        acc = self.getActiveAccount()

        self.c.execute(
            """SELECT * FROM Match_History WHERE account_name = %s AND end_date = %s""", (acc, date))

        d = defaultdict(list) 

        for row in self.c.fetchall():
            m = MatchHistoryObject(row)
            d[m.enemy_name].append(m.rating_change )

        res = {}
        
        for k, v in d.items():
    
            wins = sum(1 if rating_change > 0 else 0 for rating_change in v)
            loses = sum(1 if rating_change < 0 else 0 for rating_change in v)
            res[k] = (wins, loses)
                
        return res

    def getPointsAndRank(self):

        points = self.__fetchOne(
            """SELECT points FROM Internal_Data WHERE channel = %s""", (self.channelName,))
        rank = self.__fetchOne(
            """SELECT rank FROM Internal_Data WHERE channel = %s""", (self.channelName,))

        return (points or 0, rank or 0)

    def addNewChannel(self):

        query = ("""INSERT INTO Internal_Data\
                     (channel, active_account, points, rank, last_update)\
                     VALUES (%s, %s, %s, %s, %s)""")
        values = (self.channelName, "xyz", 0, 0, "1111-11-11 11:11:11")
        self.__query(query, values)

    def channelExistsInDb(self):

        channels = self.c.execute(
            """SELECT * FROM Internal_Data WHERE channel = %s""", (self.channelName,))
        self.c.fetchone()

        return self.c.rowcount > 0
