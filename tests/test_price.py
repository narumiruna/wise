from wise.price import get_wise_prices, Price

from typing import List


def test_get_wise_prices():
    target_amount = 1000
    target_currency = 'USD'
    source_currency = 'GBP'

    prices = get_wise_prices(target_amount=target_amount,
                             target_currency=target_currency,
                             source_currency=source_currency)

    assert isinstance(prices, List)
    assert isinstance(prices[0], Price)
    assert prices[0].targetAmount == target_amount
    assert prices[0].targetCurrency == target_currency
    assert prices[0].sourceCurrency == source_currency
