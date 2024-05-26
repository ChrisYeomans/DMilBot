class BotConstants:
    game_comment_dict = {}
    disconnect_message_lst = []

    def __init__(self):
        self.game_comment_dict = {
            "Genshin Impact": "Wow playing Genshin, go touch some grass",
            "Fortnite": "is playing Fortnite, looks like we got the next ninja",
            "League of Legends": "has a terminal case of League, RIP"
        }

        self.disconnect_message_lst = [
            "RNGesus has frowned upon you and you have been disconnected",
            "Get shit on nerd",
            "F"
        ]
