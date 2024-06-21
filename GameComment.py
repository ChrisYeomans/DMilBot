from __future__ import annotations
import discord
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Bot import Bot


class GameComment:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def run(self, before: discord.channel, after: discord.channel):
        game_comment_dict = self.bot.constants.game_comment_dict
        print("presence update")
        for activity in after.activities:
            print(activity.name)
            if activity.name in game_comment_dict \
                    and activity not in before.activities \
                    and self.presence_update_cooldown_done(after.name, 600) \
                    and self.presence_update_cooldown_done("global", 60):
                tc = self.bot.client.get_channel(self.bot.general_channel_id)
                await tc.send(f"{after.name} {game_comment_dict[activity.name]}")
                break

    def presence_update_cooldown_done(self, member_name: str, cooldown_length: int) -> bool:
        print(
            f"cooldown update {member_name} {self.bot.member_presence_cooldowns[member_name] if member_name in self.bot.member_presence_cooldowns else 'new'}")
        now: datetime = datetime.now()
        if member_name in self.bot.member_presence_cooldowns:
            timediff = now - self.bot.member_presence_cooldowns[member_name]
            cooldown_done = timediff.total_seconds() // 60 > cooldown_length
            if cooldown_done:
                self.bot.member_presence_cooldowns[member_name] = now
                return True
            else:
                return False
        else:
            self.bot.member_presence_cooldowns[member_name] = now
        return True
