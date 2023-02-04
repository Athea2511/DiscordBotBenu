import asyncio
import discord
from discord import Guild
from discord.commands import slash_command, Option
from discord.ext import commands

import os




class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("Modul: Help geladen!")

    @slash_command()
    async def help_load(self, ctx):
        active = True
        guild: Guild = self.bot.get_guild(os.getenv('SERVER_GUILD_ID'))
        mod = guild.get_role(os.getenv('MODERATOR_ROLE_ID'))
        admin = guild.get_role(os.getenv('ADMIN_ROLE_ID'))
        news_writer = guild.get_role(os.getenv('NEWS_ROLE_ID'))
        print(active)
        # Embeds
        hilfe = discord.Embed(title='***Hilfe zum BenuBot:***', colour=0x008141)
        hilfe.add_field(name='`!help`', value='zeigt diese Hilfe an\r\n')
        hilfe.add_field(name='`!team`', value='zeigt Team Mitglieder an\r\n')
        hilfe.add_field(name='`!ball`', value='Ein wahrsager Spiel\r\n')
        hilfe.add_field(name='`!help level`', value='Zeigt die level Hilfe\r\n')
        hilfe.set_thumbnail(url=self.bot.user.avatar_url_as(size=512))
        hilfe.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url_as(size=512))

        level = discord.Embed(title='***Hilfe zum Level System***', color=0xff7f00)
        level.add_field(name='`!level <spieler>`', value='zeigt deine level und deine exp.', inline=True)
        level.add_field(name='`!rank <spieler>`', value='zeigt deinen rang, deine level und deine exp.',
                        inline=True)
        level.set_thumbnail(url=self.bot.user.avatar_url_as(size=512))
        level.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url_as(size=512))

        team = discord.Embed(title="Das Team besteht aus:", )
        team.add_field(name=f"***{mod}: ***\r\n",
                       value=f'{", ".join([member.name for member in guild.members if admin in member.roles])}\r\n')
        team.add_field(name=f"***{admin}: ***\r\n",
                       value=f'{", ".join([member.name for member in guild.members if mod in member.roles])}\r\n')

        report = discord.Embed(title="Das ist das Report Formular:", colour=0xD31B24)
        report.add_field(name="Name der Beschuldigten Person ", value=" .\r\n")
        report.add_field(name="Waren Noch andere Personen beteiligt? ", value=" .\r\n")
        report.add_field(name="nummer des regel regelverstoßes :", value=" .\r\n")
        report.add_field(name="Uhrzeit des regel regelverstoßes :", value=" .\r\n")
        report.add_field(name="namen von zeugen (wenn vorhanden) :", value=" .\r\n")
        report.add_field(name="Schilderung des vorfalls :", value="Nachweis zur belegung erwünscht "
                                                                  "(Screenshot, Foto, Aufnahme)"
                                                                  "(Bitte bedenke das du die warheit sagen musst und "
                                                                  "nicht lügen solltest, solltest du dennoch lügen kann"
                                                                  " dies zu einem bann führen)", inline=True)

        rule = discord.Embed(title="`Die Server Regeln`", colour=0xD31B24,
                             description="Die Server Leitung behält sich "
                                         "vor die Regeln zu bearbeiten.\n"
                                         "\n**Ein nicht beachten führt zu "
                                         "Konsequenzen!**")
        rule.add_field(name="Regel 1", value="Beleidigende, Sexuelle oder Rassistische Inhalte sind auf diesem"
                                             " Server nicht erwünscht, und werden mit **Strafen** geahndet.",
                       inline=True)
        rule.add_field(name="Regel 2", value="Avatare, Nicknamen und Beschreibungen dürfen keine pornographischen, "
                                             "rassistischen oder beleidigende Inhalte beinhalten.", inline=True)
        rule.add_field(name="Regel 3", value="Der Umgang mit anderen Discord Benutzern sollte stets freundlich sein. "
                                             "Angriffe gegen andere Personen, Rassistische, Sexuelle oder "
                                             "Beleidigende bemerkungen sind strengstens untersagt.", inline=True)
        rule.add_field(name="Regel 4", value="Das hinter dem Rücken gerede gegenüber Admins und allen anderen "
                                             "Mitgliedern hier "
                                             "im Discord wie z.B. wegen einer Behinderung oder sonstigen Dingen "
                                             "ist strengstens untersagt da dies Verletzung der Privatsphäre ist.",
                       inline=True)
        rule.add_field(name="Regel 5", value="Wir dulden keine Mobber die anderen Communitymitgliedern den Spielspaß "
                                             "verderben.\n"
                                             " Behandel deine Mitmenschen so, wie auch Du behandelt werden möchtest ! "
                                             "Jeder Mensch hat Gefühle !", inline=True)
        rule.add_field(name="Regel 6", value='Das Fragen nach Rängen/Rechten ist untersagt, Ränge/Rechte werden nicht '
                                             'wahllos verliehen.', inline=True)
        rule.add_field(name="Regel 7", value="Bei __*Links*__ oder *Bildern* einen Moderator, Admin oder den Owner"
                                             " um Erlaubniss fragen.", inline=True)
        rule.add_field(name="Regel 8", value="Wenn du gebeten wirst, von einem Mod, Admin oder dem Owner, etwas zu "
                                             "unterlassen, dann halte dich daran Ansonsten folgen **Konsequenzen**.",
                       inline=True)
        rule.add_field(name="Regel 9",
                       value="Wer den Anweisungen des Server-Admins bzw. der Supporter nicht folgt wird "
                             "verwarnt"
                             " und im Ernstfall gekickt. Sollte sich dies häufen, ist ein Bann zu "
                             "erwarten. **Unwissenheit Schützt vor Strafe nicht!!**", inline=True)

        rule.add_field(name="Regel 10",
                       value="Es sind alle Benutzer angehalten, die Discord-Server Regeln zu beachten. "
                             "Sollte "
                             "ein Regelverstoß von einem Benutzer erkannt werden, ist dieser umgehend "
                             "einem "
                             "Admin, Mod oder Owner zu melden.\n"
                             "Ansonsten: **Habe Spaß!**", inline=True)

        rule.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/753348181554757637/812379770847232000/shooter_gray_"
                "idle.gif")
        rule.set_footer(text="______________________\n"
                             "Durch Bestätigen der regeln akzeptierest du diese.\n"
                             "Bei Fragen wende dich an:\n"
                             "Owner: Psychoclown97\n"
                             "Admin: Athea\n")

        Ende = discord.Embed(title='***Button Menü***')
        Ende.add_field(name='**Das hilfe Menü wird geschloßen **', value='Bis Bald! ')
        Ende.set_thumbnail(url=self.bot.user.avatar_url_as(size=512))
        Ende.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url_as(size=512))
        # Embeds


def setup(bot):
    bot.add_cog(Help(bot))
