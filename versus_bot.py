from command_executer import CommandExecuter

from twitchio.ext import commands

import datetime
import logging

kozak = 'szalony_jedrzej'

def power_user(ctx: commands.Context) -> bool:
    return ctx.author.is_mod or ctx.author.is_broadcaster or (ctx.author.name == kozak)

class Bot(commands.Bot):

    def __init__(self, bot_owner, twitch_token, initial_channels):
        self.bot_owner = bot_owner
        self.initial_channels = initial_channels

        super().__init__(token=twitch_token, prefix='!', initial_channels=self.initial_channels)

    async def event_ready(self):

        logging.info(f'Logged in as | {self.nick}')
        logging.info(f'User id is | {self.user_id}')
        logging.info("Ready on channels:" + str(self.initial_channels))

    async def event_message(self, message):

        if message.echo:
            return

        try:
            await self.handle_commands(message)

        except Exception as e:
            logging.error(e)

    @commands.command()
    async def versus(self, ctx: commands.Context):

        executer = CommandExecuter(ctx.channel, power_user(ctx))

        splitted = ctx.message.content.split(' ')
        opponent = splitted[1]

        await ctx.send(executer.versus(opponent))

    @commands.command()
    async def dzisiaj(self, ctx: commands.Context):

        executer = CommandExecuter(ctx.channel, power_user(ctx))
        await ctx.send(executer.dzisiaj())

    @commands.command()
    async def wczoraj(self, ctx: commands.Context):

        executer = CommandExecuter(ctx.channel, power_user(ctx))
        await ctx.send(executer.wczoraj())

    @commands.command()
    async def dzisiaj_detale(self, ctx: commands.Context):

        executer = CommandExecuter(ctx.channel, power_user(ctx))
        await ctx.send(executer.dzisiaj_detale())

    @commands.command()
    async def wczoraj_detale(self, ctx: commands.Context):

        executer = CommandExecuter(ctx.channel, power_user(ctx))
        await ctx.send(executer.wczoraj_detale())

    @commands.command()
    async def punkty(self, ctx: commands.Context):

        executer = CommandExecuter(ctx.channel, power_user(ctx))
        await ctx.send(executer.punkty())

    @commands.command()
    async def last(self, ctx: commands.Context):

        executer = CommandExecuter(ctx.channel, power_user(ctx))
        await ctx.send(executer.last())

    @commands.command()
    async def jutro(self, ctx: commands.Context):
        await ctx.send('Jutro będzie futro widzu LIKE')

    @commands.command()
    async def konto(self, ctx: commands.Context):

        if not power_user(ctx):
            return

        try:
            channel_name = ctx.channel.name
            db_wrapper = DatabaseWrapper(channel_name)
            executer = CommandExecuter(ctx.channel, power_user(ctx))
            splitted = ctx.message.content.split(' ')
            new_active_account = splitted[1]

            db_wrapper.update_active_account(new_active_account)
            db_updater = DatabaseUpdater(db_wrapper)
            db_updater.update_database()
            # updating points always, so ppl see correct rank when changing accounts
            db_updater.update_points(new_active_account)

        except Exception as e:
            await ctx.send(on_failed_account_swap_msg(new_active_account))
            logging.error(e)
            return

        await ctx.send(executer.konto(new_active_account))