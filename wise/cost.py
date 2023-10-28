from .price import Price
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

        self.source_amount = price.source_amount
        self.source_currency = price.source_currency
        self.target_amount = price.target_amount
        self.target_currency = price.target_currency

        self.fx_rate = get_rate(self.source_currency, self.quote_currency).value

    @property
    def card_fee(self) -> float:
        return self.source_amount * self.card_fee_rate

    @property
    def total_amount(self) -> float:
        return self.source_amount + self.card_fee

    @property
    def wise_fee(self) -> float:
        return self.price.total

    @property
    def wise_fee_rate(self) -> float:
        return self.wise_fee / self.source_amount

    @property
    def total_fee(self) -> float:
        return self.card_fee + self.wise_fee

    @property
    def total_fee_rate(self) -> float:
        return self.total_fee / self.total_amount

    @property
    def miles(self) -> float:
        return self.source_amount * self.mile_rate * self.fx_rate

    @property
    def mile_price(self) -> float:
        return self.total_fee * self.fx_rate / self.miles

    def __str__(self) -> str:
        return (
            f"Add {self.target_amount:.2f} { self.target_currency}"
            f", pay with {self.source_amount:.2f} {self.source_currency}"
            f", wise fee: {self.wise_fee:.2f} {self.source_currency} ({self.wise_fee_rate * 100:.2f}%)"
            f", total fee: {self.total_fee:.2f} {self.source_currency} ({self.total_fee_rate * 100:.2f}%)"
            f", miles: {self.miles:.2f} ({self.mile_price:.4f} {self.quote_currency}/mile)"
        )
