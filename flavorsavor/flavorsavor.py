"""Add some pizzaz to your day with a dose of Flavortown culture.

This is my first venture into Red-DiscordBot cogs. The concept and codebase
was __heavily__ inspired by Twentysix26's insult cog:
    https://github.com/Twentysix26/26-Cogs/tree/master/insult
"""

from discord.ext import commands
from .utils.dataIO import fileIO
from random import choice as randchoice


class FlavorSavor:
    """Cog displays random Guy Fieri quotes."""

    def __init__(self, bot):
        self.bot = bot
        self.quotes = fileIO("data/flavorsavor/quotes.json", "load")

    @commands.group(name='savor', pass_context=True)
    async def _savor(self, context):
        """Displays a random Guy Fieri quote."""
        if context.invoked_subcommand is None:
            await self.bot.say(
                context.message.author.mention + ' ' + randchoice(self.quotes))

    @_savor.command(name='', pass_context=True)
    async def blast(self, context):
        """Displays a random Guy Fieri quote with some gusto."""
        await self.bot.say(
            context.message.author.mention + ' ' +
            randchoice(self.quotes).upper())


def setup(bot):
    bot.add_cog(FlavorSavor(bot))
