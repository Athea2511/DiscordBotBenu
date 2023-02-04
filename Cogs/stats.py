from time import time
import discord
from discord.commands import slash_command
from discord.ext import commands
from datetime import datetime, timedelta
from platform import python_version
from psutil import Process, virtual_memory
from discord import __version__ as discord_version


class Statss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.VERSION = "v0.0.1"

    @commands.Cog.listener()
    async def on_ready(self):
        print('Modul: Stats Geladen')

    @slash_command()
    async def ping(self, ctx: discord.ApplicationContext):
        start = time()
        interaction = await ctx.respond(content=f"Pong! Latenz: {round(self.bot.latency*1000)} ms.")
        messid = await interaction.original_response()
        end = time()
        await messid.edit(content=f"Pong! Latenz: {round(self.bot.latency*1000)} ms. Antwortzeit: {round((end-start)*1000)} ms.")

    @slash_command(description="Zeigt die Bot Stats")
    async def show_bot_stats(self, ctx):
        try:
            embed = discord.Embed(title="Bot stats",
                                  colour=ctx.author.colour,
                                  timestamp=datetime.utcnow())
            embed.set_thumbnail(url=self.bot.user.avatar.replace(size=512))

            proc = Process()
            with proc.oneshot():
                uptime = timedelta(seconds=time()-proc.create_time())
                cpu_time = timedelta(
                    seconds=(cpu := proc.cpu_times()).system + cpu.user)
                mem_total = virtual_memory().total / (1024**2)
                mem_of_total = proc.memory_percent()
                mem_usage = mem_total * (mem_of_total / 100)

            fields = [
                ("Bot version", self.VERSION, True),
                ("Python version", python_version(), True),
                ("pycord version", discord_version, True),
                ("Uptime", uptime, True),
                ("CPU time", cpu_time, True),
                ("Memory usage",
                 f"{mem_usage:,.3f} / {mem_total:,.0f} MiB ({mem_of_total:.0f}%)", True)
            ]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await ctx.respond(embed=embed)
        except Exception as e:
            await ctx.respond(e)


def setup(bot):
    bot.add_cog(Statss(bot))
