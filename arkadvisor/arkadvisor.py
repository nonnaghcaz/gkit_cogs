"""DESCRIPTION."""

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

    @commands.group(name='ark', pass_context=True)
    async def ark(self, context):
        if not soupAvailable:
            await self.bot.say('Sorry, you need BeautifulSoup4 installed.')
        if context.invoked_subcommand is None:
            await self.bot.say('Type `[p]help ark` for info.')

    @ark.command(name='test', pass_context=True)
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
    async def tame(self, context, dino):
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
                        img_url = self.get_kibble_image(soup)
                        method = self.get_method(soup)

                        embed = discord.Embed(
                            colour=0x9933FF, title=dino.title())
                        embed.set_thumbnail(url=img_url)
                        embed.add_field(
                            name='Taming Method', value=method)
                        embed.add_field(
                            name='Preferred Kibble', value=kibble)
                        await self.bot.say(embed=embed)
                    else:
                        await self.bot.say(
                            'Sorry, could not find your dino: {}'.format(
                                dino))

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

    def get_description(self, soup):
        return soup.find('div', {'id': 'full_description'}).find('p').getText()

    def get_method(self, soup):
        try:
            ret_val = soup.find(
                'a', {
                    'title': 'Taming', 'href': re.compile(
                        '/Taming#')}).getText()
        except Exception:
            ret_val = ''
        return ret_val

    def get_kibble(self, soup):
        try:
            ret_val = soup.find(
                'a', {'href': re.compile('/Kibble')}).get('title')
        except Exception:
            ret_val = ''
        return ret_val

    def get_kibble_image(self, soup):
        try:
            ret_val = soup.find(
                'a', {'href': re.compile('/File:Kibble')}).find('img').get(
                    'src')
        except Exception:
            ret_val = ''
        return ret_val

    def get_dossier_image(self, dino, soup):
        try:
            ret_val = soup.find(
                'a', {'href': ('/File:Dossier_' + dino.title().replace(
                    ' ', '_'))}).find('img').get('src')
        except Exception:
            ret_val = ''
        return ret_val


def setup(bot):
    bot.add_cog(ArkAdvisor(bot))
