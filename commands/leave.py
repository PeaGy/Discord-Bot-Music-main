import discord

async def setup(bot):

    @bot.tree.command(
        name="leave",
        description="Nah quả lê sủi đây"
    )
    async def leave(interaction: discord.Interaction):
        vc = interaction.guild.voice_client

        if not vc:
            embed = discord.Embed(
                description="**Quả lê không có ở voice chat**"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await vc.disconnect()

        embed = discord.Embed(
            description="**Quả lê đã cút khỏi voice chat**"
        )
        await interaction.response.send_message(embed=embed)
