from typing import List

from wise.price import Price
from wise.price import find_price
from wise.price import query_prices


def test_get_prices():
    amount = 1000
    source = "GBP"
    target = "USD"

    prices = query_prices(
        target_amount=amount,
        target_currency=target,
        source_currency=source,
    )

    price = find_price(prices, pay_in_method="VISA_CREDIT", pay_out_method="BALANCE")

    assert isinstance(prices, List)
    assert isinstance(price, Price)
    assert price.target_amount == amount
    assert price.target_currency == target
    assert price.source_currency == source
