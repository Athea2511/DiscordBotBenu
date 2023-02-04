import discord
import aiohttp

from discord.ext import commands
import random



class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("meme System Geladen")

    @commands.command(invoke_without_command=True, case_insensitive=True)
    async def meme(self, ctx):
        embed = discord.Embed(title="Meme!")
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/memes/new.json?sort=memes') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)

    @commands.command(invoke_without_command=True, case_insensitive=True)
    async def pussi(self, ctx):
        embed = discord.Embed(title="Cats!")
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/cats/new.json?sort=cat') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Meme(bot))
