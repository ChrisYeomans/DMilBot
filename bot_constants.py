from random import choice


class BotConstants:
    game_comment_dict = {}
    disconnect_message_lst = []

    def __init__(self):
        self.rng_disconnect_odds = (1.5, 20)  # (a, b) = a in b odds
        self.game_comment_dict = {
            "Genshin Impact": "Wow playing Genshin, go touch some grass",
            "Fortnite": "is playing Fortnite, looks like we got the next ninja",
            "League of Legends": "has a terminal case of League, RIP",
            "Stellaris": "fukin' space weeb..."
        }

        self.disconnect_message_lst = [
            "RNGesus has frowned upon you and you have been disconnected",
            "Get shit on nerd",
            "F"
        ]

    def rng_disconnect_message(self, member) -> str:
        return f"HAHA {member.mention} {choice(self.disconnect_message_lst)}"
