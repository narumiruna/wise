from __future__ import annotations

from loguru import logger

from .price import Price
from .price import get_wise_prices
from .utils import find_price


class Payment:

    def __init__(self):
        self.target_amount = None
        self.target_currency = None
        self.source_currency = None
        self._price = None

    @property
    def price(self) -> Price:
        if self._price is not None:
            return self._price

        prices = get_wise_prices(
            source_currency=self.source_currency,
            target_amount=self.target_amount,
            target_currency=self.target_currency,
        )

        price = find_price(prices, pay_in_method='VISA_CREDIT', pay_out_method='BALANCE')
        logger.debug(f"Price: {price}")

        self._price = price

        return price

    @property
    def source_amount(self) -> float:
        return self.price.sourceAmount

    def pay_with(self, currency: str) -> Payment:
        self.source_currency = currency
        return self

    def add(self, amount: float, currency: str) -> Payment:
        self.target_amount = amount
        self.target_currency = currency
        return self
