import discord
from random import choice
from typing import Dict, List


class BotConstants:
    game_comment_dict: Dict[str, str] = {}
    disconnect_message_lst: List[str] = []
    spam_timeout_words: List[str] = []
    spam_repeat_number: int = 3
    spam_timeout_minutes: int = 3

    def __init__(self):
        self.rng_disconnect_odds = (1.5, 20)  # (a, b) = a in b odds
        self.boon_rand_odds = (1, 25)  # (a, b) = a in b odds
        self.game_comment_dict = {
            "Genshin Impact": "Wow playing Genshin, go touch some grass",
            "Fortnite": "is playing Fortnite, looks like we got the next ninja",
            "League of Legends": "has a terminal case of League, RIP",
        }

        self.disconnect_message_lst = [
            "RNGesus has frowned upon you and you have been disconnected",
            "Get shit on nerd",
            "F",
            "Skill Issue",
            "Eat my ass"
        ]

        self.spam_timeout_words = [
            "scoreboard",
        ]

    def rng_disconnect_message(self, member: discord.Member) -> str:
        return f"HAHA {member.mention} {choice(self.disconnect_message_lst)}"

    def spam_timeout_message(self, member: discord.Member, word: str) -> str:
        return f"{member.mention} DOWN WITH THE {word.upper()}"

    def spam_timeout_reason(self) -> str:
        return "STFU"
