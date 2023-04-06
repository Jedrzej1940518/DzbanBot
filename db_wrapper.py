import os
import MySQLdb
import datetime
from collections import defaultdict

# Internal data:
# channel   active_account  points  rank    last_update

# Match_History:
# account_name  end_date_time   end_date    enemy_name  host_name   duration_in_seconds rating_change

# match fieldnames = ['end_date_time', 'enemy_name',
#                      'host_name', 'duration_in_seconds', 'rating_change']

db_host = os.environ['db_host']
db_user = os.environ['db_user']
db_password = os.environ['db_password']
db_name = os.environ['db_name'] 

class MatchHistoryObject:

    def __init__(self, row):
        self.account_name = row[0]  or ""
        self.end_date_time = row[1] or ""
        self.end_date = row[2]  or ""
        self.enemy_name = row[3] or ""
        self.host_name = row[4] or ""
        self.duration_in_seconds = row[5] or 0
        self.rating_change = row[6] or 0

class DatabaseWrapper:

    def __init__(self, channel_name):

        self.db = MySQLdb.connect(host=db_host,
                                  user=db_user, password=db_password, database=db_name)
        self.c = self.db.cursor()
        self.channel_name = channel_name
        pass

    def __query(self, query, values):

        self.c.execute(query, values)
        self.db.commit()

    def __fetchOne(self, query, values):

        self.c.execute(query, values)
        return self.c.fetchone()[0]

    def __getDbValuesFromMatch(self, match, active_account):

        date_format = "%Y-%m-%d_t%H:%M:%SZ"
        end_date_time = match['end_date_time']
        end_date = datetime.datetime.strptime(end_date_time, date_format).date()

        return (active_account, end_date_time, str(end_date), match['enemy_name'], match['host_name'],
                match['duration_in_seconds'], match['rating_change'])

    def __matchRecorded(self, match):

        active_account = self.get_active_account()
        end_date_time = match['end_date_time']
        enemy_name = match['enemy_name']

        matches = self.c.execute("""SELECT * FROM Match_History WHERE account_name = %s AND end_date_time = %s AND enemy_name = %s""",
                                 (active_account, end_date_time, enemy_name))
        self.c.fetchone()

        return self.c.rowcount > 0

    def update_write_time(self, datetime):

        self.__query("""UPDATE Internal_Data SET last_update = %s WHERE channel = %s""",
                     (datetime, self.channel_name))

    def update_rating(self, points, rank):

        self.__query("""UPDATE Internal_Data 
                  SET points = %s, rank = %s
                  WHERE channel = %s""",
                     (points, rank, self.channel_name))

    def update_active_account(self, new_active_account):
        self.__query("""UPDATE Internal_Data SET active_account = %s WHERE channel = %s""",
                     (new_active_account, self.channel_name))

    def add_match_if_not_exist(self, match, active_account):

        match_added = True

        if self.__matchRecorded(match):
            return not match_added

        query = ("""INSERT INTO Match_History\
                     (account_name, end_date_time, end_date, enemy_name, host_name, duration_in_seconds, rating_change)\
                     VALUES (%s, %s, %s, %s, %s, %s, %s)""")

        values = self.__getDbValuesFromMatch(match, active_account)
        self.__query(query, values)

        return match_added

    def get_active_account(self):
        return self.__fetchOne("""SELECT active_account FROM Internal_Data WHERE channel = %s""", (self.channel_name,))

    def get_last_update_time(self):
        return self.__fetchOne(
            """SELECT last_update FROM Internal_Data WHERE channel = %s""", (self.channel_name,))

    def get_wins_loses_vs_opponent(self, enemy_name):

        #prevent injection
        acc = self.get_active_account()
        wins = self.__fetchOne(
            """SELECT COUNT(*) FROM Match_History WHERE account_name = %s AND enemy_name = %s AND rating_change>0""", (acc, enemy_name,))

        loses = self.__fetchOne(
            """SELECT COUNT(*) FROM Match_History WHERE account_name = %s AND enemy_name = %s AND rating_change<0""", (acc, enemy_name,))

        return (wins or 0, loses or 0)

    def get_wins_loses_points_for_date(self, date):  # TODO REFACTOR THIS

        acc = self.get_active_account()

        wins = self.__fetchOne(
            """SELECT COUNT(*) FROM Match_History WHERE account_name = %s AND end_date = %s AND rating_change>0""", (acc, date,))

        loses = self.__fetchOne(
            """SELECT COUNT(*) FROM Match_History WHERE account_name = %s AND end_date = %s AND rating_change<0""", (acc, date,))

        points = self.__fetchOne(
            """SELECT SUM(rating_change) FROM Match_History WHERE account_name = %s AND end_date = %s""", (acc, date,))

        return (wins or 0, loses or 0, points or 0)
    
    def get_detailed_date(self, date):
        acc = self.get_active_account()

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

    def get_points_and_rank(self):

        points = self.__fetchOne(
            """SELECT points FROM Internal_Data WHERE channel = %s""", (self.channel_name,))
        rank = self.__fetchOne(
            """SELECT rank FROM Internal_Data WHERE channel = %s""", (self.channel_name,))

        return (points or 0, rank or 0)

    def get_last_match(self):
        acc = self.get_active_account()
        self.c.execute("""SELECT * FROM Match_History WHERE account_name = %s ORDER BY end_date_time DESC LIMIT 1""",(acc,))
        row = self.c.fetchall()[0]
        return MatchHistoryObject(row)
    
    def add_new_channel(self):

        query = ("""INSERT INTO Internal_Data\
                     (channel, active_account, points, rank, last_update)\
                     VALUES (%s, %s, %s, %s, %s)""")
        values = (self.channel_name, "xyz", 0, 0, "1111-11-11 11:11:11")
        self.__query(query, values)

    def channel_exists_in_db(self):

        channels = self.c.execute(
            """SELECT * FROM Internal_Data WHERE channel = %s""", (self.channel_name,))
        self.c.fetchone()

        return self.c.rowcount > 0
