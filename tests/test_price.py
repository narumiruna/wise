import pytest
from aiolimiter import AsyncLimiter

from wise.method import PayInMethod
from wise.method import PayOutMethod
from wise.price import Price
from wise.price import PriceRequest
from wise.price import query_price


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


@pytest.mark.asyncio
@pytest.mark.parametrize("source_currency", ["GBP", "EUR"])
@pytest.mark.parametrize("target_amount", [1000])
@pytest.mark.parametrize("target_currency", ["USD"])
async def test_price_request_async(
    target_amount: float,
    source_currency: str,
    target_currency: str,
) -> None:
    async with AsyncLimiter(1, 0.05):
        prices = await PriceRequest(
            source_currency=source_currency,
            target_amount=target_amount,
            target_currency=target_currency,
        ).do()

    assert isinstance(prices, list)
    for price in prices:
        assert isinstance(price, Price)
        assert price.source_currency == source_currency
        assert price.target_amount == target_amount
        assert price.target_currency == target_currency
