from __future__ import annotations
import discord
from typing import TYPE_CHECKING, Generator
if TYPE_CHECKING:
    from Bot import Bot


class BotCommands:
    def __init__(self, bot: Bot, setup_test_commands: bool):
        self.bot: Bot = bot
        self.tree: discord.app_commands.CommandTree = discord.app_commands.CommandTree(bot.client)
        self.tree.clear_commands(guild=discord.Object(id=bot.guild_id))
        if setup_test_commands:
            self.setup_test_commands(self.tree)

    def setup_test_commands(self, tree):
        @tree.command(name="ping", description="Get a pongs", guild=discord.Object(id=self.bot.guild_id))
        async def ping(interaction: discord.interactions):
            await interaction.response.send_message("Pongs!!")

        @tree.command(name="game", guild=discord.Object(id=self.bot.guild_id))
        async def game_check(_interaction):
            users: Generator[discord.Member] = self.bot.client.get_all_members()
            for user in users:
                try:
                    for activity in user.activities:
                        if activity.type == discord.ActivityType.playing:
                            print(f"{user.name} is playing {activity.name}")
                    print(f"{user.name} is not playing anything.")
                except discord.NotFound:
                    print("User not found.")
