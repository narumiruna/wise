from .payment import Payment


def rates(from_curr, to_curr):
    payment = Payment().add(1000, currency=to_curr).pay_with(from_curr)
    p = payment.price
    return p.targetAmount / (p.sourceAmount - p.total)
