import discord
from discord.ext import commands


def is_not_pinned(mess):
    return not mess.pinned


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Modul: Clear geladen!")

    @commands.command(name="Clear")
    async def clear(self, ctx, limit: int = None):
        if ctx.message.author.guild_permissions.manage_messages:
            if not limit:
                await ctx.message.delete()
                kein_limit = discord.Embed(
                    title='**No Limit**', color=discord.Color.dark_orange())
                kein_limit.add_field(name='**Kein Limit**',
                                     value='Es wurde kein limit angegeben!')
                await ctx.send(embed=kein_limit, delete_after=5)
            else:
                await ctx.message.delete()
                await ctx.channel.purge(limit=limit, check=is_not_pinned)
                chat_clear = discord.Embed(
                    title='**Chat Clear**', color=discord.Color.green())
                chat_clear.add_field(name='**Anzahl**', value=f'{limit}')
                chat_clear.set_footer(
                    text=ctx.author, icon_url=ctx.author.avatar_url_as(size=512))
                await ctx.send(embed=chat_clear, delete_after=3)
        else:
            await ctx.message.delete()
            no_permission = discord.Embed(
                title='**No Permission**', color=discord.Color.dark_red())
            no_permission.add_field(name='Keine Rechte',
                                    value='```Moderator```')
            no_permission.set_footer(
                text=ctx.author, icon_url=ctx.author.avatar_url_as(size=512))
            await ctx.send(embed=no_permission)


def setup(bot):
    bot.add_cog(Clear(bot))
