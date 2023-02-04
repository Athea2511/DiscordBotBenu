import discord
import ListeID as IDs

from discord import slash_command
from discord.commands import Option
from discord.ext import commands
from discord import Guild


class Userinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Modul: Userinfo Geladen')

    @slash_command(description="Zeige Infos über einen User", name="userinfo")
    @commands.cooldown(1, 30 * 60, commands.BucketType.user)
    async def info(slef,
            ctx,
            user: Option(discord.Member, "Gib einen User an", default=None)
    ):
        if user is None:
            user = ctx.author

        roles = discord.Embed(title=f"Userinfo für {user.name}",
                              description=f'Dies ist eine Userinfo für den User {user.mention}',
                              color=0x22a7f0)
        createtime = discord.utils.format_dt(user.created_at, "R")
        joinedtime = discord.utils.format_dt(user.joined_at, "R")
        roles.add_field(name='Server beigetreten', value=joinedtime,
                        inline=True)
        roles.add_field(name='Discord beigetreten', value=createtime,
                        inline=True)
        rollen = ''
        for role in user.roles:
            if not role.is_default():
                rollen += f'{role.mention} \r\n'
        if rollen:
            roles.add_field(name='Rollen', value=rollen, inline=True)
            roles.set_thumbnail(url=user.display_avatar.url)
        await ctx.respond(embed=roles)

    @staticmethod
    def convert_time(seconds):
        if seconds < 60:
            return f"{round(seconds)} Sekunden"

        minutes = seconds / 60

        if minutes < 60:
            return f"{round(minutes)} Minuten"

        hours = minutes / 60

        if hours < 60:
            return f"{round(hours)} Stunden"

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = ctx.command.get_cooldown_retry_after(ctx)
            final = self.convert_time(seconds)
            await ctx.respond(f"Du must noch{final} warten", ephemeral=True)




    @slash_command()
    async def team(self, ctx):
        guild: Guild = self.bot.get_guild(IDs.SERVER_GUILD_ID)
        if guild:
            role = guild.get_role(IDs.MODERATOR_ROLE_ID)

            mods = discord.Embed(
                title="***Server Team: ***",
            )

            modmember= ''
            for member in role.members:
                modmember += f'{member.name} \r\n'
            if modmember:
                mods.add_field(name=f'moderatoren:', value=modmember, inline=True)
            await ctx.respond(embed=mods)
        else:
            print("Es Gab einen Fehler Beim Befehl")


# Team Liste Ende

def setup(bot):
    bot.add_cog(Userinfo(bot))
