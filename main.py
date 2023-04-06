import versus_bot
import sys
import os
import logging

twitch_token = os.environ['twitch_token']

bot_owner = 'szalony_jedrzej'
initial_channels = ['Gluhammer']
debug_channels = ['szalony_jedrzej']


def debug():
    logging.info("debugging start")
    try:
        bot = versus_bot.Bot(bot_owner, twitch_token, debug_channels)
        bot.run()
    except Exception as e:
        logging.error(e)


def release():
    logging.info("realse start")
    bot = versus_bot.Bot(bot_owner, twitch_token, initial_channels)
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
