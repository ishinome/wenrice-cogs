import discord
from redbot.core import commands

MSG_DUMP_CHANNEL_ID = 1474433960229470350

class DmLuku(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    __author__ = ["Wenrice"]
    __version__ = "0.0.2"

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Only DMs, ignore bots
        if message.guild is not None or message.author.bot:
            return

        channel = self.bot.get_channel(MSG_DUMP_CHANNEL_ID)
        if channel is None:
            # Not cached; fetch from API
            try:
                channel = await self.bot.fetch_channel(MSG_DUMP_CHANNEL_ID)
            except discord.NotFound:
                return
            except discord.Forbidden:
                return

        await channel.send(f"{message.author}: {message.content}")
