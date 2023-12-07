from pydantic import BaseModel

from .price import Price
from .price import PriceRequest
from .price import find_price


class Cost(BaseModel):
    price: Price
    card_fee_rate: float = 0.015
    reward_rate: float = 0.1

    @property
    def card_fee(self) -> float:
        return self.price.source_amount * self.card_fee_rate

    @property
    def wise_fee_rate(self) -> float:
        return self.price.total / self.price.source_amount

    @property
    def total_fee(self) -> float:
        return self.card_fee + self.price.total

    @property
    def total_fee_rate(self) -> float:
        return self.total_fee / (self.price.source_amount + self.card_fee)

    @property
    def cost_per_mile(self) -> float:
        return self.total_fee / (self.price.source_amount * self.reward_rate)

    def __str__(self) -> str:
        return (
            f"Add {self.price.target_amount:.2f} { self.price.target_currency}"
            f", pay with {self.price.source_amount:.2f} {self.price.source_currency}"
            f", wise fee: {self.price.total:.2f} {self.price.source_currency} ({self.wise_fee_rate * 100:.2f}%)"
            f", total fee: {self.total_fee:.2f} {self.price.source_currency} ({self.total_fee_rate * 100:.2f}%)"
            f", cost per mile: {self.cost_per_mile:.4f}"
        )


def get_cost(
    source: str,
    amount: float,
    target: str,
    pay_in_method: str = "VISA_CREDIT",
    pay_out_method: str = "BALANCE",
) -> Cost:
    prices = PriceRequest(
        source_currency=source,
        target_amount=amount,
        target_currency=target,
    ).do()
    price = find_price(
        prices,
        pay_in_method=pay_in_method,
        pay_out_method=pay_out_method,
    )
    return Cost(price=price)
