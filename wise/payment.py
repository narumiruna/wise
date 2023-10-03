from __future__ import annotations

from .price import get_wise_prices
from .utils import find_price


class Payment:
    def __init__(
        self,
        source_amount: float = None,
        source_currency: str = None,
        target_amount: float = None,
        target_currency: str = None,
    ):
        self.price = find_price(
            get_wise_prices(
                source_amount=source_amount,
                source_currency=source_currency,
                target_amount=target_amount,
                target_currency=target_currency,
            ),
            pay_in_method="VISA_CREDIT",
            pay_out_method="BALANCE",
        )

    @property
    def target_amount(self):
        return self.price.targetAmount

    @property
    def target_currency(self):
        return self.price.targetCcy

    @property
    def source_amount(self):
        return self.price.sourceAmount

    @property
    def source_currency(self):
        return self.price.sourceCcy
