import discord
import random
import bot_constants
from datetime import datetime, timedelta


class Bot:
    def __init__(self, is_test):
        if is_test:
            token_file_name = "test_token.txt"
            self.general_channel_id = 709082873994412046
            self.guild_id = 709082873994412042
        else:
            token_file_name = "token.txt"
            self.general_channel_id = 859917202027446294
            self.guild_id = 748840256559906878
        self.constants = bot_constants.BotConstants()
        self.member_presence_cooldowns = {}
        self.member_spam_check = {}

        self.token = open(token_file_name, 'r').read().strip()
        intents = discord.Intents.all()
        intents.members = True
        self.client = discord.Client(intents=intents)
        tree = discord.app_commands.CommandTree(self.client)
        self.setup_commands(tree)

        @self.client.event
        async def on_message(message):
            await self.check_timeout_spam(message)

        @self.client.event
        async def on_voice_state_update(member, before, after):
            await self.rng_disconnect(member, before, after)

        @self.client.event
        async def on_presence_update(before, after):
            game_comment_dict = self.constants.game_comment_dict
            print("presence update")
            for activity in after.activities:
                print(activity.name)
                if activity.name in game_comment_dict \
                        and activity not in before.activities \
                        and self.presence_update_cooldown_done(after.name, 600) \
                        and self.presence_update_cooldown_done("global", 60):
                    tc = self.client.get_channel(self.general_channel_id)
                    await tc.send(f"{after.name} {game_comment_dict[activity.name]}")
                    break

        @self.client.event
        async def on_ready():
            await tree.sync(guild=discord.Object(id=self.guild_id))
            print("Server is Ready!")

    def presence_update_cooldown_done(self, member_name: str, cooldown_length: int):
        print(
            f"cooldown update {member_name} {self.member_presence_cooldowns[member_name] if member_name in self.member_presence_cooldowns else 'new'}")
        now = datetime.now()
        if member_name in self.member_presence_cooldowns:
            timediff = now - self.member_presence_cooldowns[member_name]
            cooldown_done = timediff.total_seconds() // 60 > cooldown_length
            if cooldown_done:
                self.member_presence_cooldowns[member_name] = now
                return True
            else:
                return False
        else:
            self.member_presence_cooldowns[member_name] = now
        return 3600000

    async def rng_disconnect(self, member, before, after):
        if not before.channel and after.channel:
            user_rand = random.randint(1, 200)
            print(f"User: {member.name} joined voice channel: {after.channel} with user_rand: {user_rand}")
            if user_rand > 190:
                await member.move_to(None)
                tc = self.client.get_channel(self.general_channel_id)
                await tc.send(f"HAHA {member.mention} {random.choice(self.constants.disconnect_message_lst)}")

    async def check_timeout_spam(self, message):
        member_name = message.author.name
        message_text = str(message.content)
        print(member_name, message_text)
        if member_name in self.member_spam_check:
            print(self.member_spam_check[member_name])
            self.member_spam_check[member_name] += [message_text]
        else:
            self.member_spam_check[member_name] = [message_text]
        if len(self.member_spam_check[member_name]) >= 3:
            if all(i.lower() == "scoreboard" for i in self.member_spam_check[member_name]):
                try:
                    self.member_spam_check[member_name] = []
                    await message.channel.send(f"{message.author.mention} DOWN WITH THE SCOREBOARD")
                    await message.author.timeout(timedelta(minutes=5), reason="STFU")
                except:
                    print("Error, maybe permissions?")




    def setup_commands(self, tree):
        @tree.command(name="ping", description="Get a pongs", guild=discord.Object(id=self.guild_id))
        async def ping(interaction):
            await interaction.response.send_message("Pongs!!")

        @tree.command(name="game", guild=discord.Object(id=self.guild_id))
        async def game_check(interaction):
            users = self.client.get_all_members()
            for user in users:
                try:
                    for activity in user.activities:
                        if activity.type == discord.ActivityType.playing:
                            print(f"{user.name} is playing {activity.name}")
                    print(f"{user.name} is not playing anything.")
                except discord.NotFound:
                    print("User not found.")

    def run(self):
        self.client.run(self.token)
