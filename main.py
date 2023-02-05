import versusBot
import sys
import os
import logging

authToken = os.environ['authToken']

botOwner = 'szalony_jedrzej'
initialChannels = ['Gluhammer']
debugChannels = ['szalony_jedrzej']


def debug():
    logging.info("debugging start")
    bot = versusBot.Bot(botOwner, authToken, debugChannels)
    bot.run()


def release():
    logging.info("realse start")
    bot = versusBot.Bot(botOwner, authToken, initialChannels)
    bot.run()


def main():

    logging.basicConfig(filename='logs.log',
                        encoding='utf-8',
                        level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    args = sys.argv
    print(f'args = {args}')

    if len(args) > 1:
        if args[1] == '--release':
            release()
            return

    debug()

main()
