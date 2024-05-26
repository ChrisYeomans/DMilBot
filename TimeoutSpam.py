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
        if len(self.bot.member_spam_check[member_name]) >= self.bot.constants.spam_repeat_number:
            for word in self.bot.constants.spam_timeout_words:
                if all(i.lower() == word for i in self.bot.member_spam_check[member_name]):
                    try:
                        self.bot.member_spam_check[member_name] = []
                        await message.channel.send(self.bot.constants.spam_timeout_message(message.author, word))
                        await message.author.timeout(
                            timedelta(minutes=self.bot.constants.spam_timeout_minutes),
                            reason=self.bot.constants.spam_timeout_reason()
                        )
                    except Exception as e:
                        print(f"Error {e}")