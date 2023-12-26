from wise.currency import Currency
from wise.currency import CurrencyRequest
from wise.currency import query_currency


def test_currency_request() -> None:
    currencies = CurrencyRequest().do()

    assert len(currencies) > 0
    for currency in currencies:
        assert isinstance(currency, Currency)


def test_get_currency() -> None:
    currencies = query_currency()

    assert len(currencies) > 0
    assert isinstance(currencies[0], Currency)
