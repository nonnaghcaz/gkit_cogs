"""What, do you want a..."""

import discord
from discord.ext import commands


class WannaCookie:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='wanna', invoke_without_command=True)
    async def wanna(self):
        """What, do you want a..."""
        await self.bot.say('Type `[p]help wanna` for info.')

    @wanna.command(name='cookie', pass_context=True)
    async def cookie(self, context, user: discord.Member=None):
        """What, do you want a cookie?"""
        msg = 'What, do you want a cookie {}?'
        if user is not None:
            if user.id == self.bot.user.id:
                user = '... Me??'
                await self.bot.say(msg.format(user) + (
                    '\n\nERROR: No, no I do not want a cookie, '
                    'I am a bot and am not capable of eating cookies.'))
            else:
                await self.bot.say(msg.format(user.mention))
        else:
            user = context.message.author
            await self.bot.say(msg.format(user.mention))

    @wanna.command(name='goldstar', pass_context=True)
    async def goldstar(self, context, user: discord.Member=None):
        """What, do you want a gold star?"""
        msg = 'What, do you want a gold star {}?'
        if user is not None:
            if user.id == self.bot.user.id:
                user = '... Me??'
                await self.bot.say(msg.format(user) + (
                    '\n\nERROR: No, no I do not want a gold star, '
                    'I am a bot and have not material desires such '
                    'as you filthy humans.'))
            else:
                await self.bot.say(msg.format(user.mention))
        else:
            user = context.message.author
            await self.bot.say(msg.format(user.mention))


def setup(bot):
    bot.add_cog(WannaCookie(bot))
