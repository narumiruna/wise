from wise.currency import Currency
from wise.currency import CurrencyRequest


def test_currency_request() -> None:
    currencies = CurrencyRequest().do()

    assert len(currencies) > 0
    for currency in currencies:
        assert isinstance(currency, Currency)
