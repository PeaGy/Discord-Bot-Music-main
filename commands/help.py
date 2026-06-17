import discord
from discord import app_commands
from discord.ext import commands

class HelpDropdown(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.select(
    placeholder="Select to view the commands",
    options=[
        discord.SelectOption(
            label="Information",
            emoji="<:icon8:1470588914770251806>",
            value="info"
        ),
        discord.SelectOption(
            label="Commands",
            emoji="<:command8:1470588859896299780>",
            value="commands"
        ),
    ]
)
    async def select_callback(
        self,
        interaction: discord.Interaction,
        select: discord.ui.Select
    ):
        value = select.values[0]
        if value == "info":
            embed = discord.Embed(
            description=(
            "📢 **Information**\n\n"
            "Máy phát nhạc của học viện Tracen. "
            "The original code was developed by the Eva Music Bot, inspired by the Lara Bot. "
            "Pearto supports YouTube, SoundCloud, and Spotify.\n\n"
            "Created by **PeaGy**"
        )
    )
        elif value == "commands":
            embed = discord.Embed(
        description=(
            "❗ **Commands**\n\n"
            "```ansi\n"
            "\u001b[32mHere are the music commands:\u001b[0m\n"
            "```\n"
            "`/play` **:** Play music\n"
            "`/pause` **:** Pause music\n"
            "`/resume` **:** Resume music\n"
            "`/skip` **:** Skip song\n"
            "`/stop` **:** Stop music\n"
            "`/loop` **:** Loop song\n"
            "`/247` **:** Stay in voice channel\n"
            "`/autoplay` **:** Smart autoplay\n"
            "`/radio` **:** Play radio station\n"
            "`/lyric` **:** Show lyrics Music\n"
            "`/connect` **:** Connect to voice channel\n"
        )
    )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1461031433689759826/1470602546371493950/uma-musume-agnes-tachyon.gif"
        )
        await interaction.response.edit_message(embed=embed, view=self)
class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @app_commands.command(
        name="help",
        description="Show Help Panel"
    )
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            description=(
        "**🤓 Help Panel**\n"
        "\n"
        "**🗣️❓ Máy phát nhạc Tracen là gì?**\n"
        "Tracen Jukebox là bot phát nhạc hiện đại được thiết kế để mang đến trải nghiệm âm nhạc tuyệt vời nhất "
        "chất lượng âm nhạc cao cùng với các tính năng thông minh như autoplay, "
        "24/7 mode, và multi-platform support gồm **Spotify, YouTube, "
        "and SoundCloud**.\n\n"
        "**⭐ Available Categories**\n"
        "ℹ️ **:** Information\n"
        "❗ **:** Commands\n"
        "🥀 **:** Support"
    )
)
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1461031433689759826/1470602546371493950/uma-musume-agnes-tachyon.gif"
        )
        await interaction.response.send_message(
            embed=embed,
            view=HelpDropdown()
        )
async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
