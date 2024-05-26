from __future__ import annotations
import discord
from random import choice
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from Bot import Bot


class BotStatus:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def new_bot_status(self):
        await self.bot.client.change_presence(
            activity=discord.Game(name=f"with {choice(self.get_hot_boy_vip_names())}'s Balls"))

    def get_hot_boy_vip_names(self) -> List[str]:
        role_name = "HotBoy V.I.P's"
        guild = self.bot.client.get_guild(self.bot.guild_id)
        role = discord.utils.get(guild.roles, name=role_name)
        return [e.name for e in role.members]
