"""And so the lord said to me, BASTA!

I'm telling you, IT'S ENOUGH! BASTA, SATAN! BASTA
"""

import discord
from discord.ext import commands


class BASTA:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='basta', pass_context=True)
    async def _basta(self, context):
        if context.invoked_subcommand is None:
            await self.bot.say("Type `[p]help basta` for info.")

    @_basta.command(name='user', pass_context=True)
    async def user(self, context, user: discord.Member=None):
        if user is None:
            user = context.message.author
        await self.bot.say('BASTA, ' + user.mention + '! BASTA!')

    @_basta.command(name='satan', pass_context=True)
    async def satan(self, context):
        """Display the word of the basta."""
        await self.bot.say('BASTA, SATAN! BASTA!')

    @_basta.command(name='santa', pass_context=True)
    async def santa(self, context):
        """Display the word of the basta with some gusto."""
        await self.bot.say('BASTA, SANTA! BASTA!')


def setup(bot):
    bot.add_cog(BASTA(bot))
