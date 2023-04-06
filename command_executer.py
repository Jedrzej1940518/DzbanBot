from db_wrapper import DatabaseWrapper
from db_updater import DatabaseUpdater

from messages import *

import random
from datetime import datetime, timedelta

class CommandExecuter:

    def __init__(self, channel, power_user: bool):
        self._channel_name = channel.name
        self._db = DatabaseWrapper(self._channel_name)
        self._db_updater = DatabaseUpdater(self._db)
        self._power_user = power_user
        self.account_name = self._db.get_active_account()
        
    def versus(self, opponent):

        if not opponent.isalnum() or opponent == "versus":
            return ""
        
        self._db_updater.update_database(self._power_user)

        [wins, loses, points] = self._db.get_wins_loses_vs_opponent(opponent)
        return versus_msg(self.account_name, wins, loses, points, opponent)

    def dzisiaj(self):

        self._db_updater.update_database(self._power_user)
        todays_date = datetime.now().date()
        [wins, loses, point_sum] = self._db.get_wins_loses_points_for_date(todays_date)

        return today_msg(self.account_name, wins, loses, point_sum)

    def wczoraj(self):

        self._db_updater.update_database(self._power_user)
        yesterday_date = datetime.now().date() - timedelta(days = 1)
        [wins, loses, point_sum] = self._db.get_wins_loses_points_for_date(yesterday_date)

        return yesterday_msg(self.account_name, wins, loses, point_sum)

    def dzisiaj_detale(self):
        
        self._db_updater.update_database(self._power_user)
        todays_date = datetime.now().date()
        [results, points] = self._db.get_detailed_date(todays_date)
        msg = ""
        for enemy_name, [wins, loses] in results.items(): #todo add points
            msg += detailed_match_msg(enemy_name, wins, loses)
        if msg != "":
            msg += f"[{points:+}p.] " + emote_points(points)
        return msg
    
    def wczoraj_detale(self):
        self._db_updater.update_database(self._power_user)
        yesterday_date = datetime.now().date() - timedelta(days = 1)
        [results, points] = self._db.get_detailed_date(yesterday_date)
        msg = ""
        for enemy_name, [wins, loses] in results.items(): #todo add poitns
            msg += detailed_match_msg(enemy_name, wins, loses)
        if msg != "":
            msg += f"[{points:+}p.] " + emote_points(points)
        return msg
        
    def konto(self, new_active_account):
        self._db_updater.update_database(self._power_user)
        [points, rating]  = self._db.get_points_and_rank()
        return update_account_msg(new_active_account, points, rating)

    def punkty(self):
        self._db_updater.update_database(self._power_user)
        [points, _]  = self._db.get_points_and_rank()
        return points_msg(self.account_name, points)

    def last(self):
        self._db_updater.update_database(self._power_user)
        m  = self._db.get_last_match()
        return last_match_msg(m)