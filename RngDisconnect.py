from __future__ import annotations
from random import randint
import discord
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Bot import Bot


class RngDisconnect:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def run(self, member, before: discord.channel, after: discord.channel):
        if not before.channel and after.channel:
            user_rand = randint(1, self.bot.constants.rng_disconnect_odds[1] * 10)
            print(f"User: {member.name} joined voice channel: {after.channel} with user_rand: {user_rand}")
            if user_rand > (self.bot.constants.rng_disconnect_odds[1] - self.bot.constants.rng_disconnect_odds[0]) * 10:
                await member.move_to(None)
                tc = self.bot.client.get_channel(self.bot.general_channel_id)
                await tc.send(self.bot.constants.rng_disconnect_message(member))
