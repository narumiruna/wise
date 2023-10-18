from .price import get_price


def get_rate(from_curr: str, to_curr: str, amount: float = 1000):
    price = get_price(
        source_currency=from_curr, target_amount=amount, target_currency=to_curr
    )
    return price.midRate
