from .payment import Payment


def rates(base_curr: str, quote_curr: str) -> float:
    if base_curr == quote_curr:
        return 1.0
    payment = Payment().add(1000, currency=quote_curr).pay_with(base_curr)
    p = payment.price
    return p.targetAmount / (p.sourceAmount - p.total)
