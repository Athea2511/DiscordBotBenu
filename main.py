import asyncio
import logging
import os
import sys
import traceback
from asyncio import sleep
from dotenv import load_dotenv

import discord
from discord import Guild
from discord.ext import commands
from discord.commands import Option
import ListeID as IDs
from pyfiglet import Figlet

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(
    command_prefix='!',
    case_insensitive=True,
    intents=intents

)


def is_not_pinned(mess):
    return not mess.pinned


@bot.event
async def on_ready():
    ascii_banner = Figlet(font="slant")
    asci = ascii_banner.renderText("BenuBot")
    asci2 = ascii_banner.renderText("Online")
    asciembed = discord.Embed(title="Status")
    asciembed.add_field(name=" ", value=f"```{asci}\n {asci2}```")

    print(f"Wir sind eingeloggt als User {bot.user.name}")
    bot.loop.create_task(status_task())
    channel = bot.get_channel(IDs.BOT_SENDS_ID)
    await channel.send(embed=asciembed)

# Status (spielt...) beginnt + Rainbow Rolle


async def status_task():
    while True:
        guild: Guild = bot.get_guild(IDs.SERVER_GUILD_ID)
        await bot.change_presence(activity=discord.Game('Benu Bot |/help'))
        await asyncio.sleep(8)
        member_count = guild.member_count
        await bot.change_presence(activity=discord.Game(f'Mitglieder: {member_count}'))
        await asyncio.sleep(8)
        guild: Guild = bot.get_guild(IDs.SERVER_GUILD_ID)
        if guild:
            role = guild.get_role(IDs.RAINBOW_ROLE_ID)
            if role:
                if role.position < guild.get_member(bot.user.id).top_role.position:
                    await role.edit(colour=discord.Colour.random())


# Status endet + Rainbow Rolle


# WillkommensNachricht Beginn
@bot.event
async def on_member_join(member):
    if not member.bot:
        embed = discord.Embed(title=f'Willkommen auf Benu Media Pictures {member.name} 🎥',
                              description='Wir heißen dich Herzlich Willkommen auf unserem Server!\r\n'
                                          'Bitte Bestätige die Regeln des Servers um Dich zu Verifizieren.',
                              color=0x22a7f0)
        try:
            if not member.dm_channel:
                await member.create_dm()
                await member.dm_channel.send(embed=embed)
        except discord.errors.Forbidden:
            print(
                f'Es konnte keine WillkommensNachricht an {member.name} gesendet werden.')

        await sleep(60)
        for channel in member.guild.channels:
            if channel.name.startswith("All"):
                await channel.edit(name=f'All Members:{member.guild.member_count}')
                break


@bot.event
async def on_member_remove(member):
    if not member.bot:
        await sleep(60)
        for channel in member.guild.channels:
            if channel.name.startswith("All"):
                await channel.edit(name=f'All Members:{member.guild.member_count}')
                break


# WillkommensNachricht Ende


# Rainbow rolle geben beginn
@bot.command()
@commands.has_role(IDs.ASCHE_ROLE_ID)
async def rainbow(ctx):
    guild: Guild = bot.get_guild(IDs.SERVER_GUILD_ID)
    membera = ctx.message.author
    if guild:
        role = guild.get_role(IDs.RAINBOW_ROLE_ID)
        if role:
            await membera.add_roles(role)


# Rainbow Rolle geben Ende





# Restart Bot Beginn
@bot.slash_command(name="restart", description="Startet den Bot neu!")
@commands.has_role(IDs.BOTMOD_ROLE_ID)
async def restart(ctx):
    if ctx.author.bot:
        return
    else:
        await ctx.respond("*Starte Neu...*", ephemeral=True)
        await asyncio.sleep(0.5)
        python = sys.executable
        os.execl(python, python, *sys.argv)


# Stop
@bot.slash_command()
@commands.has_role(IDs.BOTMOD_ROLE_ID)
async def stop(ctx):
    await ctx.respond("*Shutting Down...*", ephemeral=True)
    await asyncio.sleep(0.5)
    exit(0)

# Error Beginn

@bot.event
async def on_application_command_error(ctx, error):
        errorembed = discord.Embed(
            title="ERROR!!!",
            colour=discord.colour.red()
        )
        errorembed.add_field(name="- -", value=error)
        channel = bot.get_channel(IDs.Bot_sends_id)
        await channel.send(embed=errorembed)


# Error Ende


# Restart Bot Ende.

if __name__ == "__main__":
    for filename in os.listdir(f"./Cogs"):
        if filename.endswith(f".py"):
            bot.load_extension(f"Cogs.{filename[:-3]}")

    load_dotenv()
    bot.run(os.getenv("TOKEN"))

