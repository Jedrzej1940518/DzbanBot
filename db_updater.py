import db_wrapper

import requests
import json
import datetime
import re
import logging
from bs4 import BeautifulSoup

class DatabaseUpdater:

    __maxRangeToGet = 20
    __secondsBetweenUpdates = 300
    __secondsBetweenUpdatesForPowerUsers=10
    
    def __init__(self, db_wrapper):
        self.db_wrapper = db_wrapper
      
    def __timePassedBetweenUpdates(self):

        now = datetime.datetime.now()
        return now - self.db_wrapper.get_last_update_time()

    def __getPointsData(self, active_acount):

        logging.info(f'getting points')

        url = f'https://h3score.com/players/profile?name={active_acount}'
        html = requests.get(url, verify=False).content
        soup = BeautifulSoup(html, 'html.parser')

        return soup

    def __getMatchData(self, page_num, size, active_acount):

        logging.info(f'getting data: {page_num}, {size}')
        url = f'https://h3score.com/players/data/last_game_results?player_name={active_acount}&page={page_num}&size={size}'
        html = requests.get(url, verify=False).content
        data = json.loads(html)
        data_items = data['data']

        return data_items

    def update_points(self, active_acount):

        try:
            soup = self.__getPointsData(active_acount)
        except Exception as e:
            logging.error(e)

        point_tag = soup.find(text=re.compile("Points \d+"))
        points = re.search("\d+", point_tag).group(0)

        rank_tag = soup.find(text=re.compile("Rank \d+"))
        rank = re.search("\d+", rank_tag).group(0)

        self.db_wrapper.update_rating(points, rank)

    def __updateMatchData(self, active_acount):

        page = 1
        range = 10
        
        while page*range <= self.__maxRangeToGet:

            try:
                matches = self.__getMatchData(page, range, active_acount)
                
                if len(matches) == 0:
                    raise Exception("unable to get any matches")
                
            except Exception as e:
                logging.error(e)
                return

            for match in matches:
                if not self.db_wrapper.add_match_if_not_exist(match, active_acount):
                    return

            page += 1
            
    def update_active_account(self, new_active_account):
        self.db_wrapper.update_active_account(new_active_account)
        self.update_points()
        
    def new_profile(self):
        logging.info("NEW PROFILE ADDED - REMEMBER TO USE !konto")
        self.db_wrapper.add_new_channel()
        
    def update_database(self, is_power_user: bool = False):

        if not self.db_wrapper.channel_exists_in_db():
            self.new_profile()
            return 
            
        t = self.__timePassedBetweenUpdates()
        
        #power users can update DB more often but still 10 seconds break to prevent pings
        if (not is_power_user) and (t.total_seconds() < self.__secondsBetweenUpdates): 
            return
        elif (is_power_user) and (t.total_seconds() < self.__secondsBetweenUpdatesForPowerUsers):
            return 
        
        self.db_wrapper.update_write_time(datetime.datetime.now())
        active_acount = self.db_wrapper.get_active_account()
        self.__updateMatchData(active_acount)
        self.update_points(active_acount)