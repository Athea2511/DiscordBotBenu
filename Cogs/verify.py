import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from captcha.image import ImageCaptcha
import random
import ListeID as IDs


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Modul: Verify Geladen')

    @slash_command()
    async def verify(self, ctx):
        sender = ctx.author

        image = ImageCaptcha(width=280, height=90)
        captcha_text = random.randint(100000, 999999)
        captcha_text = str(captcha_text)

        data = image.generate(captcha_text)
        role_has = ctx.guild.get_role(IDs.VERIFIED_ROLE_ID)

        if role_has in ctx.author.roles:
            await ctx.respond('DU bist schon verifiziert', ephemeral=True)
        else:
            image.write(captcha_text, 'CAPTCHA.png')
            await ctx.respond('Schau in den DMs')

            await sender.send('Schreibe was in der Captcha steht', file=discord.File('CAPTCHA.png'))

            print(captcha_text)

            msg = await self.bot.wait_for("message", check=lambda check: check.author.id == ctx.author.id)
            print(msg.content)

            if msg.content == captcha_text:
                await sender.send("Korrekt du bist nun verifiziert")
                role = ctx.guild.get_role(IDs.VERIFIED_ROLE_ID)

                await sender.add_roles(role)
            else:
                await sender.send('Falsch Versuch es erneut!')


def setup(bot):
    bot.add_cog(Verify(bot))
