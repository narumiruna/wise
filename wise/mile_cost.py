from .payment import Payment
from .yrate import rates


class MileCost:

    def __init__(self,
                 payment: Payment,
                 quote_currency: str = 'TWD',
                 card_fee_rate: float = 0.015,
                 miles_rate: float = 0.1):
        self.payment = payment
        self.quote_currency = quote_currency
        self.fx_rates = {}
        self.card_fee_rate = card_fee_rate
        self.miles_rate = miles_rate

    @property
    def source_currency(self):
        return self.payment.source_currency

    @property
    def target_currency(self):
        return self.payment.target_currency

    @property
    def target_amount(self):
        return self.payment.target_amount

    @property
    def source_amount(self):
        return self.payment.source_amount

    @property
    def amount(self):
        return self.source_amount * rates(self.source_currency, self.quote_currency)

    @property
    def card_fee(self):
        return self.amount * self.card_fee_rate

    @property
    def total_amount(self):
        return self.amount + self.card_fee

    @property
    def miles(self):
        return self.amount * self.miles_rate

    @property
    def wise_fee(self):
        return self.amount - self.target_amount * rates(self.target_currency, self.quote_currency)

    @property
    def total_fee(self):
        return self.card_fee + self.wise_fee

    @property
    def total_fee_rate(self):
        return self.total_fee / self.total_amount

    @property
    def mile_price(self):
        return self.total_fee / self.miles

    def __str__(self) -> str:
        format_string = 'Add {:.2f} {}'.format(self.target_amount, self.target_currency)
        format_string += ', pay {:.2f} {}'.format(self.source_amount, self.payment.source_currency)
        format_string += ' ({:.2f} {})'.format(self.amount, self.quote_currency)
        # format_string += ', wise fees: {:.2f} {}'.format(self.wise_fees, self.base_currency)
        # format_string += ', card fees: {:.2f} {}'.format(self.card_fees, self.base_currency)
        format_string += ', total fees: {:.2f} {} ({:.2f}%)'.format(self.total_fee, self.quote_currency,
                                                                    self.total_fee_rate * 100)
        format_string += ', miles: {:.2f}'.format(self.miles)
        format_string += ', mile price: {:.2f} {}/mile'.format(self.mile_price, self.quote_currency)
        return format_string
