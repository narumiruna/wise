
from wise.price import Price
from wise.price import find_price
from wise.price import query_price


def test_get_price() -> None:
    amount = 1000
    source = "GBP"
    target = "USD"

    prices = query_price(
        target_amount=amount,
        target_currency=target,
        source_currency=source,
    )

    price = find_price(prices, pay_in_method="VISA_CREDIT", pay_out_method="BALANCE")

    assert isinstance(prices, list)
    assert isinstance(price, Price)
    assert price.target_amount == amount
    assert price.target_currency == target
    assert price.source_currency == source
