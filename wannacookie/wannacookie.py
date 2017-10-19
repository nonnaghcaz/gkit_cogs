"""What, do you want a cookie?"""

import discord
from discord.ext import commands


class WannaCookie:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def wanna(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say("Type help wanna for info.")

    @wanna.command(name='cookie', pass_context=True, no_pm=True)
    async def cookie(self, ctx, user : discord.Member=None):
        msg = 'What, do you want a cookie {}?'
        if user is not None:
            if user.id == self.bot.user.id:
                user = 'Me'
                await self.bot.say(msg.format(user) + "\n\nERROR: No, no I do not want a cookie, I am a bot and am not capable of eating cookies.")
            else:
                await self.bot.say(msg.format(user.mention))
        else:
            user = ctx.message.author
            await self.bot.say(msg.format(user.mention))


def setup(bot):
    bot.add_cog(WannaCookie(bot))
