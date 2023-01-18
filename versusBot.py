from twitchio.ext import commands
import getData
import updateTable
import os

authToken = os.environ['authToken']

class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=authToken, prefix='!', initial_channels=['Gluhammer'])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        updateTable.updateTable()

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def versus(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        updateTable.updateTable()
        splitted = ctx.message.content.split(' ')
        opponent = splitted[1]
        withTime = True
        [wins, loses] = getData.versus(opponent, withTime)
        emote = getData.emoteWins(wins, loses)

        await ctx.send(f'Dzban vs. {opponent}: wygranych {wins}, przegranych {loses} {emote}')

    @commands.command()
    async def dzisiaj(self, ctx: commands.Context):
        
        updateTable.updateTable()
        [wins, loses, points] = getData.dzisiaj()
        emote = getData.emotePoints(points)

        await ctx.send(f'Dzisiaj Dzban wygrał {wins}, przegrał {loses} {emote}')

bot = Bot()
bot.run()