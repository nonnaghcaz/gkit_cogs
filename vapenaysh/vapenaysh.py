"""Vape naysh y'all.

Ordered a vape juice and can't remember what that wacky name actually
means for your vaping experience? Well come on over friendo, I've got
just the thing for you.

Can currently lookup vape juices on the following websites:

  - [x] Blue Dot Vapors (bdv)
  - [ ] White Label Juice Co. (wlj)

NOTE: Vaporizers and the associated liquids/juices are regulated under the
same laws as tobacco as of August 8, 2016. Please see the federal registrar
entry for further information:

    https://www.federalregister.gov/documents/2016/05/10/2016-10685/deeming-tobacco-products-to-be-subject-to-the-federal-food-drug-and-cosmetic-act-as-amended-by-the

Neither I, nor the Red creators, staff, or community, promote underage use of
tobacco.
"""

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
import random

DEFAULT_COLOR = 0x6441A4

VALID_COLOR_STRINGS = {
    'TWITCH PURPLE': 0x6441A4,
    'HOTLINE MIAMI PINK': 0xF765b8,
    'HOTLINE MIAMI CYAN': 0x27FDF5,
    'ZELDA PURPLE': 0xBD70D2,
    'LINK GREEN': 0x027c23
}


class VapeNayshError(Exception):
    pass


class VapeNaysh:

    def __init__(self, bot):
        self.bot = bot
        self.embed_color = DEFAULT_COLOR

    @commands.group(
        name='vape', pass_context=True, invoke_without_command=True)
    async def vape(self, context=None):
        if not soupAvailable:
            await self.bot.say('Sorry, you need BeautifulSoup4 installed.')
        # await self.bot.say('Type `[p]help vape` for info.')
        await self.bot.send_cmd_help(context)

    @vape.command(name='color', pass_context=True, hidden=True)
    @checks.serverowner_or_permissions(administrator=True)
    async def set_color(self, context, *, color: str=None):
        if not color:
            await self.bot.say(
                'Available color aliases:\n\n\t- ' +
                '\n\t- '.join([x.title() for x in VALID_COLOR_STRINGS.keys()]))
        else:
            if color[0] is '#' and len(color) is 7:
                self.embed_color = int('0x' + color[1:], 16)
            elif color[0:2].upper() in '0X':
                self.embed_color = int(color, 16)
            elif (
                    len(color.split(' ')) is 3 and
                    all([len(x) <= 3 for x in color.split(' ')])):
                # convert rgb triple to hex
                pass
            elif (
                    color.isnumeric() and
                    int(color) > 0 and
                    int(color, 16) <= 0xFFFFFF):
                self.embed_color = int(color)
            elif color.upper() in VALID_COLOR_STRINGS.keys():
                self.embed_color = VALID_COLOR_STRINGS[color.upper()]
            else:
                self.embed_color = DEFAULT_COLOR

            embed = discord.Embed(colour=self.embed_color)
            embed.add_field(
                name='Color changed!', value=(
                    context.message.author.mention +
                    ' changed the embed color to {}'.format(self.embed_color)))
            await self.bot.say(embed=embed)

    @vape.command(
        name='bdv', aliases=['bluedot', 'bluedotvapors'])
    async def bdv(self, *, flavor: str):
        """Search for a flavor on Blue Dot Vapor's website."""

        # DEBUG
        print('\n\n' + '*' * 72 + '\n\n')
        print('[vape.bdv] flavor: {}'.format(flavor))
        print('\n\n' + '*' * 72 + '\n\n')

        if flavor.upper() in 'ABOUT':
            pass
        elif flavor.upper() in 'CONTACT':
            pass
        elif flavor.upper() in ['SHIP', 'SHIPPING', 'PROCESSING']:
            url = 'https://www.bluedotvapors.com/'
            ship_str = 'ERROR'
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status is 200:
                        data = await response.text()
                        soup = BeautifulSoup(data, 'html.parser')
                        ship_str = self.get_processing_message(soup, 0)
            await self.bot.say('[PROCESSING] Blue Dot Vapors: ' + ship_str)
        else:
            await self.get_flavor(flavor, 0)

    @vape.command(name='wlj', aliases=['whitelabel', 'whitelabeljuiceco'])
    async def wlj(self, *, flavor: str):
        """Search for a flavor on White Label Juice Co.'s website."""
        await self.get_flavor(flavor, 1)

    async def get_flavor(self, flavor, mode):
        """Core method. Performs query, embed building, and output."""
        if not flavor:
            await self.bot.say("Sorry, you must specify a flavor.")
        else:
            # Determine the correct url
            if mode is 0:
                url = (
                    'https://www.bluedotvapors.com/' +
                    'collections/eliquid/products/' +
                    flavor.replace(' ', '-'))
            elif mode is 1:
                url = (
                    'https://whitelabeljuiceco.com/' +
                    'collections/whitelabel-juice/products/' +
                    flavor.replace(' ', '-')) + '-100ml'
            else:
                self.bot.say(
                    "I don't know how this happened, but an invalid mode was "
                    "passed to `get_flavor()` method. Please notify "
                    "Gannon#0851.")
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status is 200:
                        data = await response.text()
                        soup = BeautifulSoup(data, 'html.parser')

                        description = self.get_description(soup, mode)
                        rating = self.get_rating(soup, mode)
                        rating_str = (
                            (':fire:' * rating) +
                            (':heavy_multiplication_x:' * (5 - rating)))

                        reviews = self.get_reviews(soup, mode)
                        reviews_str = ' _**~' + str(reviews) + ' reviews**_'

                        img_url = 'http:' + self.get_image(soup, mode)

                        if rating >= 4 and reviews > 10:
                            tag = ':boom:'
                        elif rating < 3:
                            tag = ':zzz:'
                        else:
                            tag = ''

                        name = self.get_name(soup, mode)
                        name_str = '_**' + name + '**_ ' + tag

                        embed = discord.Embed(
                            colour=self.embed_color, title=name_str)
                        embed.set_thumbnail(url=img_url)
                        embed.add_field(
                            name='Buy', value=url)
                        embed.add_field(
                            name='Description', value=description)
                        embed.add_field(
                            name='Rating', value=(rating_str + reviews_str))
                        await self.bot.say(embed=embed)
                    else:
                        await self.bot.say(
                            'Sorry, could not find your flavor: {}'.format(
                                flavor))

    def get_rating(self, soup, mode):
        if mode is 0:
            return int(float(soup.find(
                'div', {'itemprop': 'aggregateRating'}).find(
                    'span').find(
                        'meta', {'itemprop': 'ratingValue'}).get(
                            'content')))
        elif mode is 1:
            return int(float(soup.find(
                'meta', {'itemprop': 'ratingValue'}).get('content')))
        return -1

    def get_reviews(self, soup, mode):
        if mode is 0:
            return int(soup.find(
                'div', {'itemprop': 'aggregateRating'}).find(
                    'span').find(
                        'meta', {'itemprop': 'reviewCount'}).get('content'))
        elif mode is 1:
            return int(soup.find('meta', {
                'itemprop': 'reviewCount'}).get('content'))
        return -1

    def get_name(self, soup, mode):
        if mode is 0 or mode is 1:
            return soup.find('h1', {'itemprop': 'name'}).getText()
        return ''

    def get_description(self, soup, mode):
        if mode is 0:
            return soup.find('div', {
                'id': 'full_description'}).find('p').getText()
        elif mode is 1:
            return soup.find('div', {
                'itemprop': 'description'}).find('p').getText()
        return ''

    def get_image(self, soup, mode):
        if mode is 0:
            return soup.find('img', {'id': 'productPhotoImg'}).get('src')
        elif mode is 1:
            imgs = soup.find_all(
                'img', {'class': 'ProductImg-product'})
            return imgs[random.randint(0, len(imgs))].get('src')
        return ''

    def get_processing_message(self, soup, mode):
        if mode is 0:
            return soup.find(
                'div', {'id': 'welcome-text'}).find(
                    'div').find('p').find('span').getText()
        elif mode is 1:
            pass
        return ''

    def get_about(self, soup, mode):
        if mode is 0:
            pass
        elif mode is 1:
            pass
        return ''

    def get_contact(self, soup, mode):
        if mode is 0:
            pass
        elif mode is 1:
            pass
        return ''


def setup(bot):
    bot.add_cog(VapeNaysh(bot))
