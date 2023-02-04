import discord
import os
import aiosqlite

from discord.ext import commands
from discord.commands import slash_command, Option
channel_lvl = os.getenv('lvl_CHANNEL_ID')
Live_channel = 746091041316405299
All_rights = 756162476743065661

async def get_games(ctx: discord.AutocompleteContext):
    async with aiosqlite.connect("user.db") as db:
        async with db.execute("SELECT game_name FROM games")as cursor:
            result = await cursor.fetchall()
            nun = []
            for i in result:
                nun.append(i[0])
    return nun


class Live(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = f"main.db"

    @commands.Cog.listener()
    async def on_ready(self):
        print("Live System Geladen")
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS games(
                game_name STRING, 
                serial_number INTEGER PRIMARY KEY
                )
                """
            )

    @slash_command()
    @discord.default_permissions(kick_members=True)
    async def live(
        self, 
        ctx, 
        game: Option(str, "Gib das Game an", autocomplete=get_games, default=None)
        ):
        guild: discord.Guild = self.bot.get_guild(os.getenv('SERVER_GUILD_ID'))

        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("SELECT * FROM games WHERE game_name = ?", (game,)) as cursor:
                await cursor.fetchall()
            specific = game

        if game.lower() in specific.keys():
            print("gamelower")
            Ctxs = discord.Embed(title=f"{game} wurde Ausgewählt")
            Ctxs.add_field(name="Ausgewählt", value=f"Du hast Erfolgreich {game} ausgewählt")
            await ctx.send(embed=Ctxs)
            live_channel = guild.get_channel(Live_channel)
            await live_channel.edit(name=f"{game} On Air")
            await live_channel.set_permissions(ctx.guild.default_role, view_channel=True)

        else:
            noctx = discord.Embed(title="Kein Spiel Angegeben", color=0x0000ff)
            noctx.add_field(name="Spiel nicht vorhanden", value="Bitte ein vorhandenes Spiel Angeben")
            await ctx.send(embed=noctx)

    @commands.command()
    async def Offline(self, ctx):
        guild: discord.Guild = self.bot.get_guild(os.getenv('SERVER_GUILD_ID'))
        Ctxxs = discord.Embed(title="Du bist Offline")
        Ctxxs.add_field(name="Offline ", value=f"Der Channel wurde erfolgreich zurückgesetzt")
        await ctx.send(embed=Ctxxs)
        live_channels = guild.get_channel(Live_channel)
        await live_channels.edit(name=f"🎮Ingame On Air🎮")
        await live_channels.set_permissions(ctx.guild.default_role, view_channel=False)
        return



def setup(bot):
    bot.add_cog(Live(bot))
