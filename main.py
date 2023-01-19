import versusBot
import sys

__channelName = 'Gluhammer'
__channelId = 36912126

__debugChannelName = 'szalony_jedrzej'
__debugChannelId = 133916932

def debug():
    print("debugging start")
    bot = versusBot.Bot(__debugChannelName, __debugChannelId)
    bot.run()

def release():
    print("realse start")
    bot = versusBot.Bot(__channelName, __channelId)
    bot.run()

def main():
    args = sys.argv
    print(f'args = {args}')
    
    if len(args) > 1:
        if args[1] == '--release':
            release()
            return
   
    debug()

main()