from random import randint


class RngDisconnect:
    def __init__(self, bot):
        self.bot = bot

    async def run(self, member, before, after):
        if not before.channel and after.channel:
            user_rand = randint(1, self.bot.constants.rng_disconnect_odds[1]*10)
            print(f"User: {member.name} joined voice channel: {after.channel} with user_rand: {user_rand}")
            if user_rand > (self.bot.constants.rng_disconnect_odds[1] - self.bot.constants.rng_disconnect_odds[0])*10:
                await member.move_to(None)
                tc = self.bot.client.get_channel(self.bot.general_channel_id)
                await tc.send(self.bot.constants.rng_disconnect_message(member))
