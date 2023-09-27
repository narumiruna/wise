from typing import List

from wise.price import Price
from wise.price import get_wise_prices


def test_get_wise_prices():
    target_amount = 1000
    target_currency = "USD"
    source_currency = "GBP"

    prices = get_wise_prices(
        target_amount=target_amount,
        target_currency=target_currency,
        source_currency=source_currency,
    )

    assert isinstance(prices, List)
    assert isinstance(prices[0], Price)
    assert prices[0].targetAmount == target_amount
    assert prices[0].targetCcy == target_currency
    assert prices[0].sourceCcy == source_currency
