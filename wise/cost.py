from pydantic import BaseModel
from pydantic import Field

from .price import Price
from .price import PriceRequest
from .price import find_price


class Cost(BaseModel):
    price: Price
    card_fee_percent: float = Field(default=1.5)
    reward_rate: float = Field(default=0.1)

    @property
    def card_fee(self) -> float:
        return self.price.source_amount * self.card_fee_percent / 100

    @property
    def wise_fee_percent(self) -> float:
        return 100 * self.price.total / self.price.source_amount

    @property
    def fee(self) -> float:
        return self.card_fee + self.price.total

    @property
    def fee_percent(self) -> float:
        return 100 * self.fee / (self.price.source_amount + self.card_fee)

    @property
    def cost_per_mile(self) -> float:
        return self.fee / (self.price.source_amount * self.reward_rate)

    def __str__(self) -> str:
        return (
            f"Add {self.price.target_amount:.2f} { self.price.target_currency}"
            f", pay {self.price.source_amount:.2f} {self.price.source_currency}"
            f", wise fee: {self.price.total:.2f} {self.price.source_currency} ({self.wise_fee_percent:.2f}%)"
            f", total fee: {self.fee:.2f} {self.price.source_currency} ({self.fee_percent:.2f}%)"
            f", cost per mile: {self.cost_per_mile:.4f}"
        )


def create_cost(
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
