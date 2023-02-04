import discord
from discord.ext import commands
import aiosqlite
from discord import slash_command
from PIL import ImageFont, ImageDraw
from easy_pil import Editor, load_image_async, Font, Text
import os


def get_level(xp):  # rechnet das aktuelle level
    lvl = 0
    amount = 10

    while True:
        xp -= amount
        if xp < 0:
            return lvl

        lvl += 1
        amount *= 2.2  # level 1 10 level 2 32 level 3 81 level 4 187 level 5 422 level 6 937


def get_xp(level):  # rechnet die xp für level
    xp = 0
    amount = 10

    for i in range(level):
        xp += amount
        amount *= 2.2

    return round(xp) if xp > 0 else amount


def get_xp_for_next_level(xp):  # rechnet wieviel noch fehlen
    level = get_level(xp)
    return get_xp(level + 1) - xp


# rechnet, wieviele xp seit dem letzten level up gesammelt wurden.
def get_xp_for_level(xp):
    return xp - get_xp(get_level(xp))


class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = f"main.db"

    @commands.Cog.listener()
    async def on_ready(self):
        print("Modul: Level Geladen")
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS users(
                user_name STRING,
                user_id INTEGER PRIMARY KEY, 
                msg_count INTEGER DEFAULT 0,
                level INTEGER DEFAULT 0,
                xp INTEGER DEFAULT 0
                )
                """
            )

    async def check_user(self, user_id, user_name):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                "INSERT OR IGNORE INTO users(user_id, user_name) VALUES (?,?)", (
                    user_id, user_name,)
            )
            await db.commit()

    async def get_xps(self, user_id, user_name):
        await self.check_user(user_id, user_name)
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()

        return result[0]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not message.guild:
            return

        await self.check_user(message.author.id, message.author.name)
        async with aiosqlite.connect(self.DB) as db:

            await db.execute(
                "UPDATE users SET msg_count = msg_count + 1, xp = xp + ? WHERE user_id = ?", (
                    1, message.author.id)
            )
            await db.commit()

        # check level up
        new_xp = await self.get_xps(message.author.id, message.author.name)
        level = message.guild.get_role(os.getenv('ASCHE_ROLE_ID'))
        level1 = message.guild.get_role(os.getenv('JUNGER_ROLE_ID'))
        level2 = message.guild.get_role(os.getenv('PHOENIX_ON_FIRE_ROLE_ID'))
        level3 = message.guild.get_role(os.getenv('SENIOR_PHOENIX_ROLE_ID'))
        level4 = message.guild.get_role(os.getenv('FAWKES_ROLE_ID'))
        level5 = message.guild.get_role(os.getenv('LEVEL5_ROLE_ID'))
        level6 = message.guild.get_role(os.getenv('LEVEL6_ROLE_ID'))
        lvl = get_level(new_xp)

        new_lvl = get_level(new_xp)
        old_lvl = get_level(new_xp - 1)
        lvl_nachricht = f'<@{message.author.id}> Du bist nun Level **{lvl}**. Du bekommst:'
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                "UPDATE users SET level = ? WHERE user_id = ?", (int(
                    lvl), message.author.id)
            )
            await db.commit()

        # create level up card
        font = ImageFont.truetype("fonts/Blood2.ttf", 150)
        fonts = ImageFont.truetype("fonts/Blood2.ttf", 153)
        font_small = ImageFont.truetype("fonts/Blood2.ttf", 50)
        font_smalls = ImageFont.truetype("fonts/Blood2.ttf", 70)
        poppins = Font.poppins(size=30)

        xps = await self.get_xps(message.author.id, message.author.name)
        lvls = get_level(xps)

        color_nic = "#880000"

        big_text = Font.poppins(size=50, variant="bold")
        bigs_text = Font.poppins(size=52, variant="bold")
        bigger_text = Font.poppins(size=90, variant="bold")
        small_text = Font.poppins(size=40, variant="bold")
        smalls_text = Font.poppins(size=30, variant="bold")
        biggers_text = Font.poppins(size=95, variant="bold")

        background = Editor("space.png").resize((800, 250))
        avatar = await load_image_async(message.author.display_avatar.url)
        circle_avatar = Editor(avatar).resize((200, 200)).circle_image()

        background.paste(circle_avatar, (25, 25))

        user_data = {  # Most likely coming from database or calculation
            "name": f"{message.author.name}",  # The user's name
            "xp": xps,
            "level": lvls,
            # "rank":
        }
        background.text(
            (270, 80), user_data["name"], font=font_small, color=color_nic)

        background.text(
            (270, 150),
            "Du erreichst Level: ",
            font=font_smalls,
            color=color_nic,
        )

        background.text(
            (700, 130),
            f"{lvls} ",
            font=font,
            color="#6441a5",
        )

        file = discord.File(fp=background.image_bytes, filename="level_up.png")
        # end create

        if old_lvl == new_lvl:
            return

        if new_lvl == 1:  # Level 1 10xp
            await message.author.remove_roles(level)
            await message.author.add_roles(level1)
            await message.channel.send(file=file)

        elif new_lvl == 2:  # Level 2 32xp
            await message.author.add_roles(level2)
            await message.author.remove_roles(level1)
            await message.channel.send(file=file)

        elif new_lvl == 3:  # Level 3 81xp
            await message.author.add_roles(level3)
            await message.author.remove_roles(level2)
            await message.channel.send(file=file)

        elif new_lvl == 4:  # Level 4 187xp
            await message.author.add_roles(level4)
            await message.author.remove_roles(level3)
            await message.channel.send(file=file)

        elif new_lvl == 5:  # Level 5 422xp
            await message.author.add_roles(level5)
            await message.author.remove_roles(level4)
            await message.channel.send(file=file)

        elif new_lvl == 6:  # Level 6 937xp
            await message.author.add_roles(level6)
            await message.author.remove_roles(level5)
            await message.channel.send(file=file)

    @slash_command(name="ranklist" , description="Listet die Top 3 User auf")
    async def ranklist(self, ctx):
        desc = ""
        counter = 1
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute(
                    "SELECT user_id, xp FROM users WHERE msg_count > 0 ORDER BY xp DESC LIMIT 3"
            ) as cursor:
                async for user_id, xp in cursor:
                    desc += f"{counter}.<@{user_id}> - {xp} XP\n"
                    counter += 1

        embed = discord.Embed(
            title="Rangliste",
            description=desc,
            color=discord.Color.yellow()

        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Level(bot))



                 
                  


                                    