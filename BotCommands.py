import discord


class BotCommands:
    def __init__(self, client, bot, setup_test_commands):
        self.bot = bot
        self.tree = discord.app_commands.CommandTree(client)
        self.tree.clear_commands(guild=discord.Object(id=bot.guild_id))
        if setup_test_commands:
            self.setup_test_commands(self.tree)

    def setup_test_commands(self, tree):
        @tree.command(name="ping", description="Get a pongs", guild=discord.Object(id=self.bot.guild_id))
        async def ping(interaction):
            await interaction.response.send_message("Pongs!!")

        @tree.command(name="game", guild=discord.Object(id=self.bot.guild_id))
        async def game_check(interaction):
            users = self.bot.client.get_all_members()
            for user in users:
                try:
                    for activity in user.activities:
                        if activity.type == discord.ActivityType.playing:
                            print(f"{user.name} is playing {activity.name}")
                    print(f"{user.name} is not playing anything.")
                except discord.NotFound:
                    print("User not found.")
