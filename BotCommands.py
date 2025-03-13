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
        self.setup_music_commands(self.tree)
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

    def setup_music_commands(self, tree):
        @tree.command(name="play", guild=discord.Object(id=self.bot.guild_id))
        async def play(interaction: discord.interactions, name: str):
            await self.bot.music_player.play(interaction, name)

        @tree.command(name="stop", guild=discord.Object(id=self.bot.guild_id))
        async def stop(interaction: discord.interactions):
            await self.bot.music_player.stop(interaction)

        @tree.command(name="skip", guild=discord.Object(id=self.bot.guild_id))
        async def skip(interaction: discord.interactions):
            await self.bot.music_player.skip(interaction)

        @tree.command(name="queue", guild=discord.Object(id=self.bot.guild_id))
        async def queue(interaction: discord.interactions):
            await self.bot.music_player.queue(interaction)

        @tree.command(name="playing", guild=discord.Object(id=self.bot.guild_id))
        async def playing(interaction: discord.interactions):
            await self.bot.music_player.playing(interaction)