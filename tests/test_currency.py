import pytest
from aiolimiter import AsyncLimiter

from wisest.currency import Currency
from wisest.currency import CurrencyRequest


def test_currency_request() -> None:
    currencies = CurrencyRequest().do_sync()

    assert len(currencies) > 0
    for currency in currencies:
        assert isinstance(currency, Currency)


@pytest.mark.asyncio
async def test_currency_request_async() -> None:
    async with AsyncLimiter(1, 0.05):
        currencies = await CurrencyRequest().do()

    assert len(currencies) > 0
    for currency in currencies:
        assert isinstance(currency, Currency)
