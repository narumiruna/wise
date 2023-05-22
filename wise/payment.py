from __future__ import annotations

from loguru import logger

from .price import Price
from .rate import get_wise_prices
from .utils import get_bank_transfer_in_balance_out


class Payment:

    def __init__(self):
        self.target_amount = None
        self.target_currency = None
        self.source_amount = None
        self.source_currency = None
        self.price = None

    def pay_with(self, currency: str) -> Payment:
        self.source_currency = currency
        return self

    def add(self, amount: float, currency: str) -> Payment:
        self.target_amount = amount
        self.target_currency = currency
        return self

    def get_price(self) -> Price:
        if self.price is not None:
            return self.price

        prices = get_wise_prices(
            source_currency=self.source_currency,
            target_amount=self.target_amount,
            target_currency=self.target_currency,
        )

        self.price = get_bank_transfer_in_balance_out(prices)
        logger.debug(f"Price: {self.price}")

        return self.price

    def get_amount(self) -> float:
        return self.get_price().sourceAmount

    def get_total_fees(self) -> float:
        return self.get_price().total
