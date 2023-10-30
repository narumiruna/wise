from .price import Price
from .price import get_price
from .rate import get_rate


class Cost:
    def __init__(
        self,
        price: Price,
        quote_currency: str = "TWD",
        card_fee_rate: float = 0.015,
        mile_rate: float = 0.1,
    ):
        self.price = price
        self.quote_currency = quote_currency
        self.card_fee_rate = card_fee_rate
        self.mile_rate = mile_rate

        self.source_amount = price.sourceAmount
        self.source_currency = price.sourceCcy
        self.target_amount = price.targetAmount
        self.target_currency = price.targetCcy

        self.card_fee = self.source_amount * self.card_fee_rate
        self.total_amount = self.source_amount + self.card_fee
        self.wise_fee = self.price.total
        self.wise_fee_rate = self.wise_fee / self.source_amount
        self.total_fee = self.card_fee + self.wise_fee
        self.total_fee_rate = self.total_fee / self.total_amount

        fx_rate = get_rate(self.source_currency, self.quote_currency).value
        self.miles = self.source_amount * self.mile_rate * fx_rate
        # or self.total_fee / (self.source_amount * self.mile_rate)
        self.mile_price = self.total_fee * fx_rate / self.miles

    def __str__(self) -> str:
        return (
            f"Add {self.target_amount:.2f} { self.target_currency}"
            f", pay with {self.source_amount:.2f} {self.source_currency}"
            f", wise fee: {self.wise_fee:.2f} {self.source_currency} ({self.wise_fee_rate * 100:.2f}%)"
            f", total fee: {self.total_fee:.2f} {self.source_currency} ({self.total_fee_rate * 100:.2f}%)"
            f", miles: {self.miles:.2f} ({self.mile_price:.4f} {self.quote_currency}/mile)"
        )


def get_cost(source: str, amount: float, target: str) -> Cost:
    price = get_price(
        source_currency=source,
        target_amount=amount,
        target_currency=target,
    )

    return Cost(price)
