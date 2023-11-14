from .price import Price
from .price import get_price


class Cost:
    def __init__(
        self, price: Price, card_fee_rate: float = 0.015, mile_rate: float = 0.1
    ):
        self.price = price
        self.card_fee_rate = card_fee_rate
        self.mile_rate = mile_rate

    def __str__(self) -> str:
        card_fee = self.price.source_amount * self.card_fee_rate
        total_amount = self.price.source_amount + card_fee
        wise_fee_rate = self.price.total / self.price.source_amount
        total_fee = card_fee + self.price.total
        total_fee_rate = total_fee / total_amount
        cost_per_mile = total_fee / (self.price.source_amount * self.mile_rate)

        return (
            f"Add {self.price.target_amount:.2f} { self.price.target_currency}"
            f", pay with {self.price.source_amount:.2f} {self.price.source_currency}"
            f", wise fee: {self.price.total:.2f} {self.price.source_currency} ({wise_fee_rate * 100:.2f}%)"
            f", total fee: {total_fee:.2f} {self.price.source_currency} ({total_fee_rate * 100:.2f}%)"
            f", cost per mile: {cost_per_mile:.4f}"
        )


def get_cost(source: str, amount: float, target: str) -> Cost:
    price = get_price(
        source_currency=source,
        target_amount=amount,
        target_currency=target,
    )
    return Cost(price)
