import discord

async def setup(bot):

    @bot.tree.command(
        name="loop",
        description="♾️ Toggle Loop Music"
    )
    async def loop(interaction: discord.Interaction):

        vc = interaction.guild.voice_client
        if not vc or not vc.is_playing():
            embed = discord.Embed(
                title="Không có nhạc đang phát"
            )
            return await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

        if not hasattr(bot, "♾️ looping"):
            bot.looping = False

        bot.looping = not bot.looping

        description = (
            "✅ Loop ON"
            if bot.looping
            else "❌ Loop OFF"
        )

        embed = discord.Embed(description=description)

        await interaction.response.send_message(embed=embed)
