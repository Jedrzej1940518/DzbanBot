from twitchio.ext import commands
import getData
import updateTable
import os

authToken = os.environ['authToken']

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=authToken, prefix='!', initial_channels=['Gluhammer'])

    async def event_ready(self):

        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        updateTable.updateTable()

    async def event_message(self, message):

        if message.echo:
            return

        await self.handle_commands(message)

    @commands.command()
    async def versus(self, ctx: commands.Context):

        updateTable.updateTable()
        splitted = ctx.message.content.split(' ')
        opponent = splitted[1]
        [wins, loses] = getData.versus(opponent)
        emote = getData.emoteWins(wins, loses)

        await ctx.send(f'Stary vs. {opponent}: wygranych {wins}, przegranych {loses} {emote}')

    @commands.command()
    async def dzisiaj(self, ctx: commands.Context):
        
        updateTable.updateTable()
        [wins, loses, points] = getData.dzisiaj()
        emote = getData.emotePoints(points)

        await ctx.send(f'Dzisiaj Dzban wygrał {wins}, przegrał {loses}, punkty {points:+} {emote}')

    @commands.command()
    async def punkty(self, ctx: commands.Context):
        
        updateTable.updateTable()
        [points, rank] = getData.getRating()

        await ctx.send(f'Punkty Glusia: {points} => TOP {rank} HOTA peepoBlush')

bot = Bot()
bot.run()