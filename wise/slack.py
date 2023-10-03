import os

from dotenv import find_dotenv
from dotenv import load_dotenv
from loguru import logger
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from .cost import Cost


class SlackBot:
    def __init__(self, token: str, channel: str = "#wise", threshold: float = 0.02):
        self.client = WebClient(token=token)
        self.channel = channel
        self.threshold = threshold

    def check(self, cost: Cost) -> None:
        if cost.total_fee_rate <= self.threshold:
            format_string = f"[{cost.source_currency}]"
            format_string += f" total fee rate {cost.total_fee_rate:.2%} is below threshold {self.threshold:.2%}!"
            try:
                self.client.chat_postMessage(channel=self.channel, text=format_string)
            except SlackApiError as e:
                logger.error(f"Got an error: {e.response['error']}")

    @classmethod
    def from_env(cls):
        load_dotenv(find_dotenv())
        token = os.environ.get("SLACK_BOT_TOKEN")
        return cls(token=token)
