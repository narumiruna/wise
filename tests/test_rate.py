from wise import Rate
from wise import RateHistoryRequest
from wise import RateRequest
from wise import query_rate
from wise import query_rate_history


def test_rate_request() -> None:
    source = "EUR"
    target = "USD"

    rate = RateRequest(
        source=source,
        target=target,
    ).do()

    assert isinstance(rate, Rate)
    assert rate.source == source
    assert rate.target == target


def test_rate_history_request() -> None:
    source = "EUR"
    target = "USD"
    length = 10

    rates = RateHistoryRequest(
        source=source,
        target=target,
        length=length,
        resolution="daily",
        unit="day",
    ).do()

    assert len(rates) == length
    for rate in rates:
        assert isinstance(rate, Rate)
        assert rate.source == source
        assert rate.target == target


def test_query_rate() -> None:
    rate = query_rate(source="EUR", target="USD")

    assert rate.source == "EUR"
    assert rate.target == "USD"


def test_query_rate_history() -> None:
    rates = query_rate_history(
        source="EUR",
        target="USD",
        length=10,
        resolution="daily",
        unit="day",
    )

    assert len(rates) == 10
    assert rates[0].source == "EUR"
    assert rates[0].target == "USD"
