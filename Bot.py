import discord
from bot_constants import BotConstants
from GameComment import GameComment
from RngDisconnect import RngDisconnect
from BotCommands import BotCommands
from TimeoutSpam import TimeoutSpam


class Bot:
    def __init__(self, is_test):
        self.token: str = None
        self.general_channel_id: int = None
        self.guild_id: int = None
        self.client: discord.Client = None
        self.member_presence_cooldowns = {}
        self.member_spam_check = {}

        self.basic_setup(is_test)
        self.rng_disconnect = RngDisconnect(self)
        self.constants = BotConstants()
        self.timeout_spam = TimeoutSpam(self)
        self.bot_commands = BotCommands(self.client, self, is_test)
        self.game_comment = GameComment(self)

        @self.client.event
        async def on_message(message):
            await self.timeout_spam.run(message)

        @self.client.event
        async def on_voice_state_update(member, before, after):
            await self.rng_disconnect.run(member, before, after)

        @self.client.event
        async def on_presence_update(before, after):
            await self.game_comment.run(before, after)

        @self.client.event
        async def on_ready():
            await self.bot_commands.tree.sync(guild=discord.Object(id=self.guild_id))
            print("Server is Ready!")

    def basic_setup(self, is_test):
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
