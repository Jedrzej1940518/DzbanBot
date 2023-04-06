from db_wrapper import DatabaseWrapper
from db_updater import DatabaseUpdater

import messages

import random
from datetime import datetime, timedelta

class CommandExecuter:

    def __init__(self, channel_name):
        self._channel_name = channel_name
        self._db_wrapper = DatabaseWrapper(channel_name)
        self._db_updater = DatabaseUpdater(db_wrapper)
        self.account_name = self.db.get_active_account()
        
    def versus(self, opponent, power_user: bool):

        if not opponent.isalnum() or opponent == "versus":
            return ""
        
        self.db_updater.update_database(is_power_user)

        [wins, loses] = self.db.get_wins_loses_vs_opponent(opponent)
        return versus_msg(self.account_name, wins, loses, opponent)

    def dzisiaj(self, power_user: bool):

        self.db_updater.update_database(is_power_user)
        todays_date = datetime.datetime.now().date()
        [wins, loses, point_sum] = self.db.get_wins_loses_points_for_date(todays_date)

        return today_msg(self.account_name, wins, loses, point_sum)

    def wczoraj(self, power_user: bool):

        self.db_updater.update_database(is_power_user)
        yesterday_date = datetime.datetime.now().date() - timedelta(days = 1)
        [wins, loses, point_sum] = self.db.get_wins_loses_points_for_date(yesterday_date)

        return yesterday_msg(self.account_name, wins, loses, point_sum)

    def dzisiaj_detale(self, power_user: bool):
        
        self.db_updater.update_database(is_power_user)
        todays_date = datetime.datetime.now().date()
        results = self.db.get_detailed_date(todays_date)
        msg = ""
        for enemy_name, [wins, loses] in results.items(): #todo add points
            msg += detailed_match_msg(enemy_name, wins, loses)
        return msg
    
    def wczoraj_detale(self, power_user: bool):
        self.db_updater.update_database(is_power_user)
        yesterday_date = datetime.datetime.now().date() - timedelta(days = 1)
        results = self.db.get_detailed_date(yesterday_date)
        msg = ""
        for enemy_name, [wins, loses] in results.items(): #todo add poitns
            msg += detailed_match_msg(enemy_name, wins, loses)
        return msg
        
    def konto(self, new_active_account, power_user: bool):
        self.db_updater.update_database(is_power_user)
        [points, rating]  = self.db.get_points_and_rank()
        return update_account_msg(new_active_account, points, rating)

    def punkty(self, power_user: bool):
        self.db_updater.update_database(is_power_user)
        [points, _]  = self.db.get_points_and_rank()
        return points_msg(self.account_name, points)

    def last(self, power_user: bool):
        self.db_updater.update_database(is_power_user)
        m  = self.db.get_last_match()
        return last_match_msg(m)