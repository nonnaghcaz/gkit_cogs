"""Feed your Salty Bet gambling addiction."""

import discord
from discord.ext import commands


class SaltyDebt:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def salty(self, ctx):
        """Feed your Salty Bet gambling addiction."""
        if ctx.invoked_subcommand is None:
            await self.bot.say("Type `[p]help salty` for info.")

    @salty.command(name='balance', pass_context=True)
    async def balance(self, ctx):
        """Check SB bank balance."""
        pass

    @salty.command(name='bet', pass_context=True)
    async def bet(self, ctx):
        """Bet on an SB contender."""
        pass


def setup(bot):
    bot.add_cog(SaltyDebt(bot))
