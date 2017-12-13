"""Add some pizzaz to your day with a dose of Flavortown culture.

This is my first venture into Red-DiscordBot cogs. The concept and codebase
was __heavily__ inspired by Twentysix26's insult cog:
    https://github.com/Twentysix26/26-Cogs/tree/master/insult
"""

from discord.ext import commands
from .utils.dataIO import fileIO
from random import choice as randchoice

BASE_STRING = '{u} {fl}{q}{fr}'


class FlavorSavor:
    """Cog displays random Guy Fieri quotes."""

    def __init__(self, bot):
        self.bot = bot
        self.quotes = fileIO("data/flavorsavor/quotes.json", "load")

    @commands.group(name='savor', pass_context=True)
    async def savor(self, context):
        """Displays a random Guy Fieri quote."""
        if context.invoked_subcommand is None:
            await self.bot.say(BASE_STRING.format(
                u=context.message.author.mention,
                q=randchoice(self.quotes),
                fl='',
                fr=''))

    @savor.command(name='gusto', pass_context=True)
    async def gusto(self, context):
        """Displays a random Guy Fieri quote with bold."""
        await self.bot.say(BASE_STRING.format(
            u=context.message.author.mention,
            q=randchoice(self.quotes),
            fl='**',
            fr='**'))

    @savor.command(name='juicy', pass_context=True)
    async def juicy(self, context):
        """Displays a random Guy Fieri quote with italics."""
        await self.bot.say(BASE_STRING.format(
            u=context.message.author.mention,
            q=randchoice(self.quotes),
            fl='_',
            fr='_'))

    @savor.command(name='spicy', pass_context=True)
    async def spicy(self, context):
        """Displays a random Guy Fieri quote with bolded italics."""
        await self.bot.say(BASE_STRING.format(
            u=context.message.author.mention,
            q=randchoice(self.quotes),
            fl='_**',
            fr='**_'))

    @commands.group(name='taste', pass_context=True)
    async def taste(self, context):
        """`taste` command not yet implemented."""
        await self.bot.say(
            'Sorry, ' +
            context.message.author.mention +
            ', the `taste` command not yet implemented.')

    @taste.command(name='sweet', pass_context=True)
    async def sweet(self, context):
        """`sweet` sub-command not yet implemented."""
        await self.bot.say(
            'Sorry, ' +
            context.message.author.mention +
            ', the `sweet` sub-command not yet implemented.')

    @taste.command(name='sour', pass_context=True)
    async def sour(self, context):
        """`sour` sub-command not yet implemented."""
        await self.bot.say(
            'Sorry, ' +
            context.message.author.mention +
            ', the `sour` sub-command not yet implemented.')

    @taste.command(name='bitter', pass_context=True)
    async def bitter(self, context):
        """`bitter` sub-command not yet implemented."""
        await self.bot.say(
            'Sorry, ' +
            context.message.author.mention +
            ', the `bitter` sub-command not yet implemented.')

    @taste.command(name='salty', pass_context=True)
    async def salty(self, context):
        """`salty` sub-command not yet implemented."""
        await self.bot.say(
            'Sorry, ' +
            context.message.author.mention +
            ', the `salty` sub-command not yet implemented.')

    @taste.command(name='umami', pass_context=True)
    async def umami(self, context):
        """`umami` sub-command not yet implemented."""
        await self.bot.say(
            'Sorry, ' +
            context.message.author.mention +
            ', the `umami` sub-command not yet implemented.')


def setup(bot):
    bot.add_cog(FlavorSavor(bot))
