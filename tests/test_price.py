from wise import PayInMethod
from wise import PayOutMethod
from wise import Price
from wise import PriceRequest
from wise import find_price


def test_price_request() -> None:
    amount = 1000
    source = "GBP"
    target = "USD"

    prices = PriceRequest(
        source_amount=amount,
        source_currency=source,
        target_currency=target,
    ).do()

    assert isinstance(prices, list)
    for price in prices:
        assert isinstance(price, Price)
        assert price.source_amount == amount
        assert price.source_currency == source
        assert price.target_currency == target

    price = find_price(prices, pay_in_method=PayInMethod.VISA_CREDIT, pay_out_method=PayOutMethod.BALANCE)
    assert isinstance(price, Price)
    assert price.source_amount == amount
    assert price.source_currency == source
    assert price.target_currency == target
