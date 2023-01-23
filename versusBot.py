from twitchio.ext import commands
from databaseWrapper import DatabaseWrapper
from databaseUpdater import DatabaseUpdater
from commandExecuter import CommandExecuter
from messages import *
import logging


def prepAndGetCommandExecuter(channel, update=True):
    channelName = channel.name
    dbWrapper = DatabaseWrapper(channelName)
    dbUpdater = DatabaseUpdater(dbWrapper)
    dbUpdater.updateDatabase()

    commandExecuter = CommandExecuter(channel, dbWrapper)

    return commandExecuter


class Bot(commands.Bot):

    def __init__(self, botOwner, authToken, initialChannels):
        self.initialChannels = initialChannels
        self.botOwner = botOwner
        super().__init__(token=authToken, prefix='!', initial_channels=self.initialChannels)

    async def event_ready(self):

        logging.info(f'Logged in as | {self.nick}')
        logging.info(f'User id is | {self.user_id}')
        logging.info("Ready on channels:" + str(self.initialChannels))

    async def event_message(self, message):

        if message.echo:
            return

        await self.handle_commands(message)

    @commands.command()
    async def versus(self, ctx: commands.Context):

        try:
            executer = prepAndGetCommandExecuter(ctx.channel)
        except Exception as e:
            logging.error(e)
            return

        splitted = ctx.message.content.split(' ')
        opponent = splitted[1]

        await ctx.send(executer.versus(opponent))

    @commands.command()
    async def dzisiaj(self, ctx: commands.Context):

        try:
            executer = prepAndGetCommandExecuter(ctx.channel)
        except Exception as e:
            logging.error(e)
            return

        await ctx.send(executer.dzisiaj())

    @commands.command()
    async def wczoraj(self, ctx: commands.Context):

        try:
            executer = prepAndGetCommandExecuter(ctx.channel)
        except Exception as e:
            logging.error(e)
            return

        await ctx.send(executer.wczoraj())

    @commands.command()
    async def dzisiaj_detale(self, ctx: commands.Context):

        try:
            executer = prepAndGetCommandExecuter(ctx.channel)
        except Exception as e:
            logging.error(e)
            return

        await ctx.send(executer.dzisiaj_detale())

    @commands.command()
    async def wczoraj_detale(self, ctx: commands.Context):

        try:
            executer = prepAndGetCommandExecuter(ctx.channel)
        except Exception as e:
            logging.error(e)
            return

        await ctx.send(executer.wczoraj_detale())

    @commands.command()
    async def punkty(self, ctx: commands.Context):

        try:
            executer = prepAndGetCommandExecuter(ctx.channel)
        except Exception as e:
            logging.error(e)
            return

        await ctx.send(executer.punkty())

    @commands.command()
    async def jutro(self, ctx: commands.Context):
        await ctx.send('Jutro będzie futro widzu LIKE')
        
    @commands.command()
    async def konto(self, ctx: commands.Context):

        if not (ctx.author.is_mod or ctx.author.is_broadcaster or (ctx.author.name == self.botOwner)):
            return

        try:
            channelName = ctx.channel.name
            dbWrapper = DatabaseWrapper(channelName)
            executer = CommandExecuter(channelName, dbWrapper)
            splitted = ctx.message.content.split(' ')
            newActiveAccount = splitted[1]

            dbWrapper.updateActiveAccount(newActiveAccount)
            dbUpdater = DatabaseUpdater(dbWrapper)
            dbUpdater.updateDatabase()
            # updating points always, so ppl see correct rank when changing accounts
            dbUpdater.updatePoints(newActiveAccount)

        except Exception as e:
            await ctx.send(onFailedAccountSwap(newActiveAccount))
            logging.error(e)
            return

        await ctx.send(executer.konto(newActiveAccount))
