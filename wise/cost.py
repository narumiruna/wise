from .payment import Payment


class Cost:

    def __init__(self, payment: Payment, card_fee_rate: float = 0.015, miles_rate: float = 0.1):
        self.payment = payment
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
    def card_fee(self):
        return self.source_amount * self.card_fee_rate

    @property
    def total_amount(self):
        return self.source_amount + self.card_fee

    @property
    def wise_fee(self):
        return self.payment.price.total

    @property
    def total_fee(self):
        return self.card_fee + self.wise_fee

    @property
    def total_fee_rate(self):
        return self.total_fee / self.total_amount

    def __str__(self) -> str:

        return (f'add {self.target_amount:.2f} {self.target_currency}'
                f', pay with: {self.source_amount:.2f} {self.source_currency}'
                f', fee: {self.total_fee:.2f} {self.source_currency} '
                f', fee rate: {self.total_fee_rate*100:.2f}')
