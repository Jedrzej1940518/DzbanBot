
import requests
import json
import datetime
import re
import logging
from databaseWrapper import DatabaseWrapper
from bs4 import BeautifulSoup

class DatabaseUpdater:

    __maxRangeToGet = 20
    __secondsBetweenUpdates = 300
    
    def __init__(self, dbWrapper):
        self.dbWrapper = dbWrapper
      
    def __timePassedBetweenUpdates(self):

        now = datetime.datetime.now()
        return now - self.dbWrapper.getLastUpdateTime()

    def __getPointsData(self, activeAcount):

        logging.info(f'getting points')

        url = f'https://h3score.com/players/profile?name={activeAcount}'
        html = requests.get(url, verify=False).content
        soup = BeautifulSoup(html, 'html.parser')

        return soup

    def __getMatchData(self, pageNum, size, activeAcount):

        logging.info(f'getting data: {pageNum}, {size}')
        url = f'https://h3score.com/players/data/lastGameResults?playerName={activeAcount}&page={pageNum}&size={size}'
        html = requests.get(url, verify=False).content
        data = json.loads(html)
        dataItems = data['data']

        return dataItems

    def updatePoints(self, activeAcount):

        try:
            soup = self.__getPointsData(activeAcount)
        except Exception as e:
            logging.error(e)

        pointTag = soup.find(text=re.compile("Points \d+"))
        points = re.search("\d+", pointTag).group(0)

        rankTag = soup.find(text=re.compile("Rank \d+"))
        rank = re.search("\d+", rankTag).group(0)

        self.dbWrapper.updateRating(points, rank)

    def __updateMatchData(self, activeAcount):

        page = 1
        range = 10
        
        while page*range <= self.__maxRangeToGet:

            try:
                matches = self.__getMatchData(page, range, activeAcount)
                
                if len(matches) == 0:
                    raise Exception("unable to get any matches")
                
            except Exception as e:
                logging.error(e)
                return

            for match in matches:
                if not self.dbWrapper.addMatchIfNotExist(match, activeAcount):
                    return

            page += 1
            
    def updateActiveAccount(self, newActiveAccount):
        self.dbWrapper.updateActiveAccount(newActiveAccount)
        self.updatePoints()
        
    def newProfile(self):
        logging.info("NEW PROFILE ADDED - REMEMBER TO USE !konto")
        self.dbWrapper.addNewChannel()
        
    def updateDatabase(self):

        if not self.dbWrapper.channelExistsInDb():
            self.newProfile()
            return 
            
        t = self.__timePassedBetweenUpdates()
            
        if t.total_seconds() < self.__secondsBetweenUpdates:
            return

        self.dbWrapper.updateWriteTime(datetime.datetime.now())
        activeAcount = self.dbWrapper.getActiveAccount()
        self.__updateMatchData(activeAcount)
        self.updatePoints(activeAcount)