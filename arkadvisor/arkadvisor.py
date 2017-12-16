"""All your ARK: Survival Evolved needs at your fingertips."""

import discord
from discord.ext import commands

from .utils import checks

try:
    # check if BeautifulSoup4 is installed
    from bs4 import BeautifulSoup
    soupAvailable = True
except ValueError:
    soupAvailable = False

import aiohttp
import re


BASE_URL = 'https://ark.gamepedia.com'


class ArkAdvisorError(Exception):
    pass


class DinoNotFoundError(ArkAdvisorError):
    pass


class ArkAdvisor:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='ark', pass_context=True, invoke_without_command=True)
    async def ark(self, context=None):
        if not soupAvailable:
            await self.bot.say('Sorry, you need BeautifulSoup4 installed.')
        await self.bot.send_cmd_help(context)

    @ark.command(name='test', pass_context=True, hidden=True)
    @checks.serverowner_or_permissions(administrator=True)
    async def _test(self, context, page=None):
        url = BASE_URL
        if page:
            url = (
                BASE_URL + '/' + page.title().replace(' ', '_'))
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status is 200:
                    data = await response.text()
                    soup = BeautifulSoup(data, 'html.parser')
                    await self.bot.say(soup.title)

    @ark.command(
        name='tame', pass_context=True, aliases=[])
    async def tame(self, context, *, dino: str):
        if not dino:
            await self.bot.say("Type `[p]help ark tame` for info.")
        elif not self.check_dino_is_tamable(dino):
            await self.bot.say(
                "Sorry, {} was not found or is not tamable.".format(dino))
        else:
            url = (
                BASE_URL + '/' + dino.title().replace(' ', '_'))
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status is 200:
                        data = await response.text()
                        soup = BeautifulSoup(data, 'html.parser')

                        kibble = self.get_kibble(soup)
                        img_url = self.get_dossier_image(soup)
                        method = self.get_method(soup)

                        title_s = len('<title>')
                        title_e = len(
                            ' - Official ARK: Survival Evolved Wiki</title>')
                        title = str(soup.title)[title_s:-title_e]

                        print('\n\n' + '*' * 72 + '\n\n')
                        print('Title:  \t' + title)
                        print('Method: \t' + method)
                        print('Kibble: \t' + kibble)
                        print('\n\n' + '*' * 72 + '\n\n')

                        if method and kibble and img_url:
                            embed = discord.Embed(
                                colour=0x6441A4,
                                title=title)
                            embed.set_thumbnail(url=img_url)
                            embed.add_field(
                                name='Taming Method', value=method)
                            embed.add_field(
                                name='Preferred Kibble', value=kibble)
                            await self.bot.say(embed=embed)
                        else:
                            await self.bot.say(
                                'Sorry, {} is not tamable.'.format(
                                    dino.title()))
                    else:
                        await self.bot.say(
                            'Sorry, could not find your dino: {}'.format(
                                dino))

    @ark.group(name='cheat', pass_context=True, invoke_without_command=True)
    async def cheat(self, context=None):
        await self.bot.send_cmd_help(context)

    @cheat.command(name='give', aliases=['giveitem', 'giveitemnum'])
    async def give(self, *, params: str=None):
        """Build a cheat string to give a player an item."""
        # TODO: Think about how to incorporate mod items w/o BP path
        if not params:
            await self.bot.say(
                'Sorry, the following parameter structures were expected:\n'
                '\t`<BlueprintPath> <Quantity> <Quality> <ForceBlueprint>`\n'
                'OR\n'
                '\t`<ItemNum> <Quantity> <Quality> <ForceBlueprint>`')
        else:
            # Parse params string by:
            #   1. Pipe (|): Aligns with ARK's method of command separation
            #   2. Space ( ): Separates individual command params
            #       NOTE: Must determine consistent method to handle multi-word
            #       item names when parsing <item>, <quantity>, <quality>
            pass

    @cheat.command(name='spawn', aliases=['dospawn', 'spawndino'])
    async def spawn(self, *, params: str=None):
        """Build a cheat string to spawn a wild dino."""
        if not params:
            pass
        else:
            # Parse params string by:
            #   1. Pipe (|): Aligns with ARK's method of command separation
            #   2. Space ( ): Separates individual command params
            #       NOTE: Must determine consistent method to handle multi-word
            #       item names when parsing <item>, <quantity>, <quality>
            pass

    @cheat.command(name='summon', aliases=['dosummon', 'summondino'])
    async def summon(self, *, params: str=None):
        """Build a cheat string to summon a tamed dino or entity."""
        if not params:
            pass
        else:
            # Parse params string by:
            #   1. Pipe (|): Aligns with ARK's method of command separation
            #   2. Space ( ): Separates individual command params
            #       NOTE: Must determine consistent method to handle multi-word
            #       item names when parsing <item>, <quantity>, <quality>
            pass

    async def check_dino_is_tamable(self, dino):
        found = False

        url = (
            BASE_URL + '/' + 'Category:Tameable_creatures')
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status is 200:
                    data = await response.text()
                    soup = BeautifulSoup(data, 'html.parser')

                    try:
                        soup.find(
                            'div', {'dir': 'ltr'}).find(
                                'div').find('div').find(
                                    'ul').find('li').find(
                                        'a', {'title': dino.replace(
                                            '_', ' ').title()}).getText()
                        found = True
                    except DinoNotFoundError:
                        pass
                else:
                    pass
        return found

    def get_method(self, soup):
        try:
            ret_val = soup.find(
                'a', {
                    'title': 'Taming', 'href': re.compile(
                        '/Taming#')}).getText()
        except Exception:
            ret_val = None
        return ret_val

    def get_kibble(self, soup):
        try:
            ret_val = soup.find(
                'a', {'href': re.compile('/Kibble\w+')}).getText()
        except Exception:
            ret_val = None
        return ret_val

    def get_kibble_image(self, soup):
        try:
            ret_val = soup.find(
                'a', {'href': re.compile('/File:Kibble')}).find('img').get(
                    'src')
        except Exception:
            ret_val = None
        return ret_val

    def get_dossier_image(self, soup):
        try:
            ret_val = soup.find(
                'a', {'href': re.compile('/File:Dossier_')}).find('img').get(
                    'src')
        except Exception:
            ret_val = None
        return ret_val


def setup(bot):
    bot.add_cog(ArkAdvisor(bot))
