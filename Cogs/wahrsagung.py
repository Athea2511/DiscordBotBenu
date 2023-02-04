import discord

import random
import asyncio


from discord.ext import commands


antworten = ['Ja', 'Nein', 'Vielleicht', 'Wahrscheinlich', 'Sieht so aus', 'Sehr wahrscheinlich',
             'Sehr unwahrscheinlich']


class Ball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Modul: Ball geladen!")

    @commands.command(name="Ball")
    async def ball(self, ctx, *, arg=None):
        if not arg:
            await ctx.message.delete()
            no_args = discord.Embed(
                title='**Keine Frage**', color=discord.Color.dark_orange())
            no_args.add_field(name='**Keine Frage**',
                              value='Es wurde Keine Frage angegeben!')
            await ctx.send(embed=no_args, delete_after=5)
        else:
            frage = f'{arg}'
            mess = await ctx.send(f'Ich versuche deine Frage `{frage}` zu beantworten.')
            await asyncio.sleep(2)
            await mess.edit(content='Ich kontaktiere das Orakel...')
            await asyncio.sleep(2)
            await mess.edit(content=f'Deine Antwort zur Frage `{frage}` lautet: `{random.choice(antworten)}`')


def setup(bot):
    bot.add_cog(Ball(bot))
