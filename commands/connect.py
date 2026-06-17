import discord
from music.player import start_idle_timer

async def setup(bot):
    @bot.tree.command(
        name="connect",
        description="Quả lê Connect To Voice Channel"
    )
    async def connect(interaction: discord.Interaction):
        if not interaction.user.voice:
            embed = discord.Embed(
                title="**You must be in a voice channel to use this command**",
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        user_channel = interaction.user.voice.channel
        vc = interaction.guild.voice_client
        if vc and vc.channel != user_channel:
            embed = discord.Embed(
                title="**Quả lê đang ở kênh voice chat khác rùi cưng**",
                description=f"I'm currently in **{vc.channel.name}**",
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        if vc and vc.channel == user_channel:
            embed = discord.Embed(
                description="**Tui đã trong voice chat rùi nè**",
            )
            await interaction.response.send_message(embed=embed)
            return
        await interaction.response.defer()
        try:
            vc = await user_channel.connect()
        except TimeoutError:
            embed = discord.Embed(
                title="Connection Timed Out",
                description="Failed to connect to the voice channel. Discord's voice servers might be slow or blocking UDP traffic."
            )
            return await interaction.followup.send(embed=embed)
        except Exception as e:
            if isinstance(e, discord.ClientException):
                vc = interaction.guild.voice_client
            else:
                embed = discord.Embed(
                    title="Failed to Connect",
                    description=f"An error occurred: `{str(e)}`"
                )
                return await interaction.followup.send(embed=embed)
        await start_idle_timer(vc, channel=interaction.channel)
        embed = discord.Embed(
            description=(
                f"**Quả lê đã có mặt tại kênh voice chat này "
                f"{user_channel.name}**"
            ),
        )
        embed.set_footer(
            text="Dùng /play Để chơi nhạc HOẶC /help Để xem tất cả lệnh"
        )
        await interaction.followup.send(embed=embed)
