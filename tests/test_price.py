from typing import List

from wise.price import Price
from wise.price import find_price
from wise.price import get_price
from wise.price import get_prices


def test_get_price():
    source = "GBP"
    amount = 1000
    target = "USD"

    price = get_price(
        source_currency=source, target_amount=amount, target_currency=target
    )

    assert price.sourceCcy == source
    assert price.targetAmount == amount
    assert price.targetCcy == target


def test_get_prices():
    amount = 1000
    source = "GBP"
    target = "USD"

    prices = get_prices(
        target_amount=amount,
        target_currency=target,
        source_currency=source,
    )

    price = find_price(prices, pay_in_method="VISA_CREDIT", pay_out_method="BALANCE")

    assert isinstance(prices, List)
    assert isinstance(price, Price)
    assert price.targetAmount == amount
    assert price.targetCcy == target
    assert price.sourceCcy == source
