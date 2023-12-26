from wise.currency import Currency
from wise.currency import query_currency


def test_get_currency() -> None:
    currencies = query_currency()

    assert len(currencies) > 0
    assert isinstance(currencies[0], Currency)
