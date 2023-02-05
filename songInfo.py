import time as _time
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from messages import *

def moj_song(user:str, dictionary):  
    
    (song, time) = dictionary[user]
    
    (hours, remainder) = divmod(time.total_seconds(), 3600)
    (minutes, seconds) = divmod(remainder, 60)

    u = user.lower()
    if u not in dictionary:
        return noSongForUserMsg(u)
    else:
        return songForUser(song, int(hours), int(minutes))

def scrapWebsite():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')


    browser = webdriver.Chrome(chrome_options=chrome_options)

    url = "https://moo.bot/r/songlist#gluhammer"
    browser.get(url)

    # Wait for 5 seconds
    _time.sleep(5)

    # Print the content of the website
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    td_elements = soup.find_all('td', {'data-id': 'information'})
    information = [td.text.strip() for td in td_elements]

    r = re.compile('(.*)By (.*) (\(.*\))')

    time_sum = datetime.timedelta()
    
    result = {}

    for i in information:
        m = r.match(i)
        song = m.group(1)
        user = m.group(2).lower()
        time = (m.group(3))[1:6]
        (m,s) = time.split(':')
        result[user] = (song, time_sum)
        time_sum += datetime.timedelta(minutes=int(m), seconds = int(s))
        
        #print("song:", song, "user: ", user, "time: ", time)

    browser.quit()
    
    return result
    