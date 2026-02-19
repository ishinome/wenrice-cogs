import asyncio
import contextlib
from typing import Literal

import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import bold

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]

EMOJIS = ["None", "🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴", "🇵", "🇶", "🇷", "🇸", "🇹"]


class Poll(commands.Cog):
    """
    make polls.
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot

    __author__ = ["Wenrice"]
    __version__ = "1.1.5"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """
        Thanks Kiutsa!
        """
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthors: {', '.join(self.__author__)}\nCog Version: {self.__version__}"

    async def red_delete_data_for_user(
        self, *, requester: RequestType, user_id: int
    ) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)

    @commands.command(name="quickpoll")
    @commands.guild_only()
    @commands.bot_has_permissions(add_reactions=True, embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def quickpoll(self, ctx: commands.Context, *, question: str):
        """
        Make a simple poll.
        """
        with contextlib.suppress(discord.Forbidden):
            await ctx.message.delete()
        if len(bold(question)) > 256:
            return await ctx.send("The question is too long.")
        embed = discord.Embed(
            title=bold(question),
        )
        embed.set_author(
            name=ctx.author.display_name, icon_url=ctx.author.display_avatar
        )
        e = await ctx.send(embed=embed)
        asyncio.sleep(1)
        await e.add_reaction("⬆")
        await e.add_reaction("⬇")

    @commands.command(name="poll", usage="[columns] <question> | <option1> | <option2> | ...")
    @commands.guild_only()
    @commands.bot_has_permissions(add_reactions=True, embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def poll(self, ctx: commands.Context, columns: int = 2, *, question: str):
        with contextlib.suppress(discord.Forbidden):
            await ctx.message.delete()

        questions = [q.strip() for q in question.split("|")]
        num = len(questions)
        if num > 21:
            return await ctx.send("You can only have 20 options in a poll")
        if num < 3:
            return await ctx.send("You need at least 2 options to make a poll")

        questions = list(zip(EMOJIS, questions))

        if len(bold(questions[0][1])) > 256:
            return await ctx.send("The question is too long.")

        embed = discord.Embed(title=bold(questions[0][1]))
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)

        # Build option lines
        option_lines = [f"{emoji} | {text}" for emoji, text in questions[1:]]

        # Clamp columns: Discord won't reliably show >3 columns anyway
        columns = max(1, min(3, columns))

        # Split evenly by count
        per_col = math.ceil(len(option_lines) / columns)
        for c in range(columns):
            chunk = option_lines[c * per_col : (c + 1) * per_col]
            if not chunk:
                continue
            embed.add_field(
                name="\u200b",            # blank header
                value="\n".join(chunk),   # lines in this column
                inline=True
            )

        e = await ctx.send(embed=embed)
        for i in range(1, num):
            await e.add_reaction(EMOJIS[i])