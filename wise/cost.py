from .payment import Payment
from .visa import get_visa_fx_rate


class Cost:

    def __init__(self, payment: Payment, base_currency: str = 'TWD'):
        self.payment = payment
        self.base_currency = base_currency
        self.fx_rates = {}

    @property
    def source_currency(self):
        return self.payment.source_currency

    @property
    def target_currency(self):
        return self.payment.target_currency

    @property
    def target_amount(self):
        return self.payment.target_amount

    def get_fx_rate(self, from_curr: str, to_curr: str):
        symbol = f'{from_curr}{to_curr}'
        if symbol in self.fx_rates.keys():
            return self.fx_rates[symbol]

        fx_rate = get_visa_fx_rate(from_curr=to_curr, to_curr=from_curr)
        self.fx_rates[symbol] = float(fx_rate.convertedAmount)
        return self.fx_rates[symbol]

    def get_amount(self) -> float:
        return self.payment.get_amount() * self.get_fx_rate(self.source_currency, self.base_currency)

    def get_total_amount(self) -> float:
        return self.get_amount() + self.get_card_fees()

    def get_card_fees(self, fee_rate: float = 0.015) -> float:
        return self.get_amount() * fee_rate

    def get_miles(self, miles_rate: float = 0.1) -> float:
        return self.get_amount() * miles_rate

    def get_wise_fees(self) -> float:
        return self.get_amount() - self.target_amount / self.get_fx_rate(self.base_currency, self.target_currency)

    def get_total_fees(self) -> float:
        return self.get_card_fees() + self.get_wise_fees()

    def get_total_fee_rate(self) -> float:
        return self.get_total_fees() / self.get_total_amount()

    def __str__(self) -> str:
        format_string = 'Add {:.2f} {}'.format(self.target_amount, self.target_currency)
        format_string += ', pay {:.2f} {}'.format(self.payment.get_amount(), self.payment.source_currency)
        format_string += ' ({:.2f} {})'.format(self.get_amount(), self.base_currency)
        # format_string += ', wise fees: {:.2f} {}'.format(self.get_wise_fees(), self.base_currency)
        # format_string += ', card fees: {:.2f} {}'.format(self.get_card_fees(), self.base_currency)
        format_string += ', total fees: {:.2f} {} ({:.2f}%)'.format(self.get_total_fees(), self.base_currency,
                                                                    self.get_total_fee_rate() * 100)
        format_string += ', miles: {:.2f}'.format(self.get_miles())
        format_string += ', mile cost: {:.2f} {}/mile'.format(self.get_total_fees() / self.get_miles(),
                                                              self.base_currency)
        return format_string
