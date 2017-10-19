"""Displays the word of the BDFL."""

import discord
from discord.ext import commands


ZEN_OF_PYTHON = """
HEREIN LIES THE WORD OF THE BDFL (as told by Tim Peters):

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
"""


class BDFL:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def assimilate(self, context):
        """Display the word of the BDFL."""
        await self.bot.say(
            'Listen close my child, ' + context.message.author.mention + '\n\n' + ZEN_OF_PYTHON)


def setup(bot):
    bot.add_cog(BDFL(bot))
