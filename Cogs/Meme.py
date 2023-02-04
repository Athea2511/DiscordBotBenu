import discord
import aiohttp
from discord.ext import commands
import random




class Hot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Hot System Geladen")

    @commands.command(invoke_without_command=True, case_insensitive=True)
    async def Hot(self, ctx):
        embed = discord.Embed(title="Hier ein sexy Bild!")
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/nsfw/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)

    @commands.command(invoke_without_command=True, case_insensitive=True)
    async def boobs(self, ctx):
        embed = discord.Embed(title="BOOBS!")
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/boobs/new.json?sort=boobs') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)

    @commands.command(invoke_without_command=True, case_insensitive=True)
    async def ass(self, ctx):
        embed = discord.Embed(title="Hier ein geiler Arsch")
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/ass/new.json?sort=ass') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)

    @commands.command(invoke_without_command=True, case_insensitive=True)
    async def pussy(self, ctx):
        embed = discord.Embed(title="Hier eine pussy")
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/pussy/new.json?sort=pussy') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)

    @commands.command(invoke_without_command=True, case_insensitive=True)
    async def sexy(self, ctx):
        embed = discord.Embed(title="Hier ein sexy bild!")
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/sexy/new.json?sort=sexy') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Hot(bot))
