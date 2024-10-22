import pytest

from wisest.method import PayInMethod
from wisest.method import PayOutMethod
from wisest.price import Price
from wisest.price import query_price


@pytest.mark.parametrize("source_currency", ["GBP", "EUR"])
@pytest.mark.parametrize("target_amount", [1000])
@pytest.mark.parametrize("target_currency", ["USD"])
@pytest.mark.parametrize("pay_in_method", [PayInMethod.VISA_CREDIT])
@pytest.mark.parametrize("pay_out_method", [PayOutMethod.BALANCE])
def test_query_price(
    target_amount: float,
    source_currency: str,
    target_currency: str,
    pay_in_method: PayInMethod,
    pay_out_method: PayOutMethod,
) -> None:
    price = query_price(
        source_currency=source_currency,
        target_amount=target_amount,
        target_currency=target_currency,
        pay_in_method=pay_in_method,
        pay_out_method=pay_out_method,
    )

    assert isinstance(price, Price)
    assert price.source_currency == source_currency
    assert price.target_amount == target_amount
    assert price.target_currency == target_currency
    assert price.pay_in_method == pay_in_method
    assert price.pay_out_method == pay_out_method
