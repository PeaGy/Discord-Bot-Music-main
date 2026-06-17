import discord
import aiohttp
import urllib.parse
import re

class MusicControl(discord.ui.View):
    def __init__(self, vc):
        super().__init__(timeout=None)
        self.vc = vc

    @discord.ui.button(label="Back", emoji="⏮️", style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        from music.player import history, queue, play_next

        # 🚫 Tidak ada lagu sebelumnya
        if len(history) < 2:
            return await interaction.response.send_message(
                "❌ No previous song available",
                ephemeral=True
            )

        # 🎵 Ambil lagu sebelumnya
        current_song = history.pop()
        previous_song = history.pop()

        # Kembalikan ke queue
        queue.appendleft(current_song)
        queue.appendleft(previous_song)

        if self.vc.is_playing() or self.vc.is_paused():
            self.vc.is_previous_action = True
            self.vc.stop()
        else:
            await play_next(interaction.client, self.vc, interaction.channel)

        await interaction.response.defer()

    # 👇 Diperbarui dengan custom emoji pause
    @discord.ui.button(label="Pause", emoji="⏸️", style=discord.ButtonStyle.secondary)
    async def pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.vc.is_playing():
            self.vc.pause()
            button.label = "Resume"
            # 👇 Menggunakan custom emoji play
            button.emoji = discord.PartialEmoji.from_str("▶️")
        else:
            self.vc.resume()
            button.label = "Pause"
            # 👇 Kembali ke custom emoji pause
            button.emoji = discord.PartialEmoji.from_str("⏸️")

        await interaction.response.edit_message(view=self)

    # 👇 Diperbarui dengan custom emoji stop
    @discord.ui.button(label="Stop", emoji="⏹️", style=discord.ButtonStyle.secondary)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        from music.player import queue, now_playing_messages

        msg = now_playing_messages.pop(interaction.guild.id, None)

        queue.clear()

        if self.vc.is_playing() or self.vc.is_paused():
            self.vc.stop_request = True
            self.vc.stop()

        if self.vc.is_connected():
            await self.vc.disconnect()

        if msg:
            embed = discord.Embed(
                description="⏹️ **Stopped Playing**"
            )
            try:
                await msg.edit(embed=embed, view=None)
            except:
                pass

        await interaction.response.defer()

    @discord.ui.button(label="Skip", emoji="⏭️", style=discord.ButtonStyle.secondary)
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.vc.is_playing() or self.vc.is_paused():
            self.vc.skip_request = True
            self.vc.stop()

        await interaction.response.defer()

    @discord.ui.button(
        label="Loop",
        emoji="🔁",
        style=discord.ButtonStyle.secondary
    )
    async def loop(self, interaction: discord.Interaction, button: discord.ui.Button):
        bot = interaction.client
        if not hasattr(bot, "looping"):
            bot.looping = False

        bot.looping = not bot.looping

        description = (
            "✅ Loop ON"
            if bot.looping
            else "❌ Loop OFF"
        )
        embed = discord.Embed(description=description)
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(
        label="Autoplay",
        emoji="🔁",
        style=discord.ButtonStyle.secondary
    )
    async def autoplay(self, interaction: discord.Interaction, button: discord.ui.Button):
        from music.player import autoplay_guilds

        guild_id = interaction.guild.id

        if guild_id in autoplay_guilds:
            autoplay_guilds.remove(guild_id)
            embed = discord.Embed(description="**Autoplay disabled**")
            return await interaction.response.send_message(embed=embed)

        autoplay_guilds.add(guild_id)
        embed = discord.Embed(description="**Autoplay enabled**")
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(
        label="Lyric",
        emoji="📝",
        style=discord.ButtonStyle.secondary
    )
    async def lyric(self, interaction: discord.Interaction, button: discord.ui.Button):
        from music.player import history

        vc = self.vc
        if not vc or not (vc.is_playing() or vc.is_paused()):
            embed = discord.Embed(description="No music is playing", color=0x2b2d31)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
            
        if len(history) == 0:
            embed = discord.Embed(description="No song info available", color=0x2b2d31)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
            
        current_song = history[-1]
        title = current_song.get("title", "Unknown")
        artist = current_song.get("author", "")
        
        await interaction.response.defer(ephemeral=True)
        
        clean_title = re.sub(r'\(.*?\)|\[.*?\]', '', title)
        clean_title = re.sub(r'(?i)(official|music video|lyric video|audio|video)', '', clean_title)
        clean_title = " ".join(clean_title.split())
        if not clean_title:
            clean_title = title
            
        clean_artist = ""
        if artist and artist != "Unknown":
            clean_artist = re.sub(r'(?i)(official|vevo|topic|- topic)', '', artist)
            clean_artist = " ".join(clean_artist.split())
            
        search_query = f"{clean_title} {clean_artist}".strip()
        query = urllib.parse.quote(search_query)
        url = f"https://lrclib.net/api/search?q={query}"
        
        lyrics = None
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers={'User-Agent': 'Mozilla/5.0'}) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data:
                            lyrics = data[0].get("syncedLyrics") or data[0].get("plainLyrics")
            except Exception:
                pass
                
        if not lyrics:
            embed = discord.Embed(description=f"❌ Không tìm thấy lời bài hát cho **{title}**.", color=0x2b2d31)
            return await interaction.followup.send(embed=embed, ephemeral=True)
            
        if len(lyrics) > 4000:
            lyrics = lyrics[:3997] + "..."
            
        embed = discord.Embed(
            title=f"🗣️ Lyrics: {title}",
            description=lyrics,
            color=0x2b2d31
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

class RadioControl(discord.ui.View):
    def __init__(self, vc):
        super().__init__(timeout=None)
        self.vc = vc
        
    @discord.ui.button(label="Down", emoji="🔉", style=discord.ButtonStyle.secondary, row=0)
    async def vol_down(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.vc.source and isinstance(self.vc.source, discord.PCMVolumeTransformer):
            self.vc.source.volume = max(0.0, self.vc.source.volume - 0.1)
            self.vc.current_volume = self.vc.source.volume
            await interaction.response.send_message(f"Volume: {int(self.vc.source.volume * 100)}%", ephemeral=True)
        else:
            await interaction.response.send_message("Volume control not available", ephemeral=True)

    # 👇 Diperbarui dengan custom emoji pause
    @discord.ui.button(label="Pause", emoji="⏹️", style=discord.ButtonStyle.secondary, row=0)
    async def pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.vc.is_playing():
            self.vc.pause()
            button.label = "Resume"
            # 👇 Menggunakan custom emoji play
            button.emoji = discord.PartialEmoji.from_str("▶️")
        else:
            self.vc.resume()
            button.label = "Pause"
            # 👇 Kembali ke custom emoji pause
            button.emoji = discord.PartialEmoji.from_str("⏸️")
        await interaction.response.edit_message(view=self)

    # 👇 Diperbarui dengan custom emoji stop
    @discord.ui.button(label="Stop", emoji="⏹️", style=discord.ButtonStyle.secondary, row=0)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        from music.player import queue, now_playing_messages
        msg = now_playing_messages.pop(interaction.guild.id, None)
        queue.clear()
        if self.vc.is_playing() or self.vc.is_paused():
            self.vc.stop_request = True
            self.vc.stop()
        if self.vc.is_connected():
            await self.vc.disconnect()
        if msg:
            embed = discord.Embed(
                description="⏹️ **Stopped Playing**"
            )
            try:
                await msg.edit(embed=embed, view=None)
            except:
                pass
        await interaction.response.defer()

    @discord.ui.button(label="Up", emoji="🔊", style=discord.ButtonStyle.secondary, row=0)
    async def vol_up(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.vc.source and isinstance(self.vc.source, discord.PCMVolumeTransformer):
            self.vc.source.volume = min(2.0, self.vc.source.volume + 0.1)
            self.vc.current_volume = self.vc.source.volume
            await interaction.response.send_message(f"Volume: {int(self.vc.source.volume * 100)}%", ephemeral=True)
        else:
            await interaction.response.send_message("Volume control not available", ephemeral=True)

    @discord.ui.button(label="Change", emoji="↪️", style=discord.ButtonStyle.secondary, row=1)
    async def change(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        
        from commands.radio import RadioView
        view = RadioView(interaction, is_change=True)
        await view.fetch_stations()
        
        if not view.stations:
            embed = discord.Embed(
                description="No radio stations found.",
                color=0x2b2d31
            )
            return await interaction.followup.send(embed=embed, ephemeral=True)
            
        view.update_components()
        
        await interaction.followup.send(embed=view.generate_embed(), view=view, ephemeral=True)