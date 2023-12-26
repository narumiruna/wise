from wise import Rate
from wise import RateHistoryRequest
from wise import RateRequest
from wise import Resolution
from wise import Unit


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
        resolution=Resolution.DAILY,
        unit=Unit.DAY,
    ).do()

    assert len(rates) == length
    for rate in rates:
        assert isinstance(rate, Rate)
        assert rate.source == source
        assert rate.target == target
