import discord
from discord.ext import commands
from random import choice as randchoice
import json


class FlavorSavor:

    def __init__(self, bot):
        self.bot = bot
        self.quotes = json.load("./data/quotes.json")

    @commands.command(pass_context=True, no_pm=True)
    async def savor(self, context):
        await self.bot.say(
            context.message.author.mention + ' ' + randchoice(self.quotes))


def setup(bot):
    bot.add_cog(FlavorSavor(bot))
