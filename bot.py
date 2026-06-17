# bot.py
import discord
from discord.ext import commands, tasks
import os
import config
import asyncio


class MusicBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True

        super().__init__(
            command_prefix="!",
            intents=intents
        )

        self.status_list = [
            "24/7 Bot Music",
            "Miễn phí cho mọi nhà",
            "dùng /play để Play Music",
            "dùng /help để thấy tất cả lệnh"
        ]
        self.status_index = 0

        # ⏳ simpan idle task per guild
        self.idle_tasks = {}

    async def setup_hook(self):
        for file in os.listdir("./commands"):
            if file.endswith(".py") and not file.startswith("_"):
                await self.load_extension(f"commands.{file[:-3]}")

        await self.tree.sync()
        print("✅ Slash commands synced")

        self.rotate_status.start()

    @tasks.loop(seconds=30)
    async def rotate_status(self):
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=self.status_list[self.status_index]
            )
        )

        self.status_index = (self.status_index + 1) % len(self.status_list)

    @rotate_status.before_loop
    async def before_rotate_status(self):
        await self.wait_until_ready()

    # ==============================
    # 🔥 AUTO DISCONNECT SYSTEM
    # ==============================

    async def start_idle_timer(self, guild: discord.Guild):
        if guild.id in self.idle_tasks:
            return

        async def idle_check():
            await asyncio.sleep(180)  # 3 phut

            vc = guild.voice_client
            if vc and not vc.is_playing():
                await vc.disconnect()
                print(f"🔌 Disconnected from {guild.name} (Idle 3 minutes)")

            self.idle_tasks.pop(guild.id, None)

        task = self.loop.create_task(idle_check())
        self.idle_tasks[guild.id] = task

    def cancel_idle_timer(self, guild: discord.Guild):
        task = self.idle_tasks.pop(guild.id, None)
        if task:
            task.cancel()

    async def on_voice_state_update(self, member, before, after):
        # Nếu bot rời khỏi kênh thoại
        if member == self.user and before.channel is not None and after.channel is None:
            # Matikan loop
            if hasattr(self, "looping"):
                self.looping = False
            
            # Tắt chế độ tự động phát
            try:
                from music.player import autoplay_guilds
                if member.guild.id in autoplay_guilds:
                    autoplay_guilds.remove(member.guild.id)
            except ImportError:
                pass


bot = MusicBot()
bot.run(config.TOKEN)
