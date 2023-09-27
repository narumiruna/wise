import asyncio
import os

import telegram


class TelegramBot:
    def __init__(self, token: str, chat_id: int):
        self.token = token
        self.chat_id = chat_id

    @classmethod
    def from_env(cls):
        token = os.getenv("BOT_TOKEN")
        chat_id = os.getenv("CHAT_ID")
        if chat_id is None:
            raise ValueError("CHAT_ID is not set")
        return cls(token, int(chat_id.strip()))

    def send(self, message: str):
        bot = telegram.Bot(self.token)
        asyncio.run(bot.send_message(self.chat_id, message, disable_notification=True))
