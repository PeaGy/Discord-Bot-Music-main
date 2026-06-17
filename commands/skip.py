import discord
from discord import app_commands
from discord.ext import commands

class Skip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="next", description="Skip To Next Song")
    async def next(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client

        if not vc or not vc.is_playing():
            embed = discord.Embed(
                description="**Không có nhạc nào đang phát**"
            )
            return await interaction.response.send_message(embed=embed)

        vc.skip_request = True
        vc.stop()

        embed = discord.Embed(
            description="⏩ **Skipped tới bài khác**"
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Skip(bot))
