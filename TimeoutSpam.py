from datetime import timedelta


class TimeoutSpam:
    def __init__(self, bot):
        self.bot = bot

    async def run(self, message):
        member_name = message.author.name
        message_text = str(message.content)
        if member_name in self.bot.member_spam_check:
            print(member_name, self.bot.member_spam_check[member_name])
            self.bot.member_spam_check[member_name] += [message_text]
        else:
            self.bot.member_spam_check[member_name] = [message_text]
        if len(self.bot.member_spam_check[member_name]) >= 3:
            if all(i.lower() == "scoreboard" for i in self.bot.member_spam_check[member_name]):
                try:
                    self.bot.member_spam_check[member_name] = []
                    await message.channel.send(f"{message.author.mention} DOWN WITH THE SCOREBOARD")
                    await message.author.timeout(timedelta(minutes=5), reason="STFU")
                except Exception as e:
                    print(f"Error {e}")