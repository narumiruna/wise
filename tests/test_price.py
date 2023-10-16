from typing import List

from wise.price import Price
from wise.price import find_price
from wise.price import get_prices


def test_get_wise_prices():
    target_amount = 1000
    target_currency = "USD"
    source_currency = "GBP"

    prices = get_prices(
        target_amount=target_amount,
        target_currency=target_currency,
        source_currency=source_currency,
    )

    pay_in_method = "VISA_CREDIT"
    pay_out_method = "BALANCE"
    price = find_price(
        prices, pay_in_method=pay_in_method, pay_out_method=pay_out_method
    )

    assert isinstance(prices, List)
    assert isinstance(price, Price)
    assert price.targetAmount == target_amount
    assert price.targetCcy == target_currency
    assert price.sourceCcy == source_currency
