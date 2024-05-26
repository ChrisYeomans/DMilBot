from random import choice


class BotConstants:
    game_comment_dict = {}
    disconnect_message_lst = []
    spam_repeat_number = 3
    spam_timeout_minutes = 3
    spam_timeout_words = []

    def __init__(self):
        self.rng_disconnect_odds = (1.5, 20)  # (a, b) = a in b odds
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
            "Eat my shorts"
        ]

        self.spam_timeout_words = [
            "scoreboard",
        ]

    def rng_disconnect_message(self, member) -> str:
        return f"HAHA {member.mention} {choice(self.disconnect_message_lst)}"

    def spam_timeout_message(self, member, word: str) -> str:
        return f"{member.mention} DOWN WITH THE {word.upper()}"

    def spam_timeout_reason(self) -> str:
        return "STFU"
