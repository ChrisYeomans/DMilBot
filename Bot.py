import discord
from datetime import datetime
from discord.ext import tasks
from typing import Dict, List
from bot_constants import BotConstants
from GameComment import GameComment
from RngDisconnect import RngDisconnect
from BotCommands import BotCommands
from TimeoutSpam import TimeoutSpam
from BotStatus import BotStatus
from MusicPlayer import MusicPlayer


class Bot:
    def __init__(self, is_test):
        self.token: str = None
        self.general_channel_id: int = None
        self.guild_id: int = None
        self.client: discord.Client = None
        self.member_presence_cooldowns: Dict[str, datetime] = {}
        self.member_spam_check: Dict[str, List[str]] = {}

        self.basic_setup(is_test)
        self.rng_disconnect: RngDisconnect = RngDisconnect(self)
        self.constants: BotConstants = BotConstants()
        self.timeout_spam: TimeoutSpam = TimeoutSpam(self)
        self.bot_commands: BotCommands = BotCommands(self, is_test)
        self.game_comment: GameComment = GameComment(self)
        self.bot_status: BotStatus = BotStatus(self)
        self.music_player: MusicPlayer = MusicPlayer(self)

        @self.client.event
        async def on_message(message: discord.Message):
            await self.timeout_spam.run(message)

        @self.client.event
        async def on_voice_state_update(member: discord.Member, before: discord.channel, after: discord.channel):
            await self.rng_disconnect.run(member, before, after)

        @self.client.event
        async def on_presence_update(before: discord.channel, after: discord.channel):
            await self.game_comment.run(before, after)

        @self.client.event
        async def on_ready():
            await self.bot_commands.tree.sync(guild=discord.Object(id=self.guild_id))
            self.bot_status_loop.start()
            print("Server is Ready!")

    @tasks.loop(hours=2)
    async def bot_status_loop(self):
        print("Status Looping")
        await self.bot_status.new_bot_status()

    def basic_setup(self, is_test: bool):
        if is_test:
            token_file_name = "test_token.txt"
            self.general_channel_id = 709082873994412046
            self.guild_id = 709082873994412042
        else:
            token_file_name = "token.txt"
            self.general_channel_id = 859917202027446294
            self.guild_id = 748840256559906878
        self.token = open(token_file_name, 'r').read().strip()
        intents = discord.Intents.all()
        intents.members = True
        self.client = discord.Client(intents=intents)

    def run(self):
        self.client.run(self.token)
