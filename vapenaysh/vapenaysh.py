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

try:
    # check if BeautifulSoup4 is installed
    from bs4 import BeautifulSoup
    soupAvailable = True
except ValueError:
    soupAvailable = False

import aiohttp


class VapeNayshError(Exception):
    pass


class VapeNaysh:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='vape', pass_context=True)
    async def vape(self, context):
        if not soupAvailable:
            await self.bot.say('Sorry, you need BeautifulSoup4 installed.')
        if context.invoked_subcommand is None:
            await self.bot.say('Type `[p]help vape` for info.')

    @vape.command(
        name='bdv', pass_context=True, aliases=['bluedot', 'bluedotvapors'])
    async def bdv(self, context, *, flavor: str):
        if not flavor:
            await self.bot.say("Type `[p]help vape bdv` for info.")
        else:
            url = (
                'https://www.bluedotvapors.com/' +
                'collections/eliquid/products/' +
                flavor)
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status is 200:
                        data = await response.text()
                        soup = BeautifulSoup(data, 'html.parser')

                        description = self.get_description(soup)
                        rating = self.get_rating(soup)
                        rating_str = (
                            (':fire:' * rating) +
                            (':heavy_multiplication_x:' * (5 - rating)))

                        reviews = self.get_reviews(soup)
                        reviews_str = ' _**~' + str(reviews) + ' reviews**_'

                        img_url = 'http:' + self.get_image(soup)

                        if rating >= 4:
                            tag = ':boom:'
                        elif rating < 3:
                            tag = ':zzz:'
                        else:
                            tag = ''

                        name = self.get_name(soup)
                        name_str = '_**' + name + '**_ ' + tag

                        embed = discord.Embed(colour=0x6441A4, title=name_str)
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

    def get_rating(self, soup):
        return int(float(soup.find(
            'div', {'itemprop': 'aggregateRating'}).find(
                'span').find(
                    'meta', {'itemprop': 'ratingValue'}).get(
                        'content')))

    def get_reviews(self, soup):
        return soup.find(
            'div', {'itemprop': 'aggregateRating'}).find(
                'span').find(
                    'meta', {'itemprop': 'reviewCount'}).get('content')

    def get_name(self, soup):
        return soup.find('h1', {'itemprop': 'name'}).getText()

    def get_description(self, soup):
        return soup.find('div', {'id': 'full_description'}).find('p').getText()

    def get_image(self, soup):
        return soup.find('img', {'id': 'productPhotoImg'}).get('src')


def setup(bot):
    bot.add_cog(VapeNaysh(bot))
