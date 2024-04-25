import pytest

from wise.rate import Rate
from wise.rate import RateHistoryRequest
from wise.rate import RateRequest
from wise.rate import Resolution
from wise.rate import Unit


@pytest.mark.parametrize("source", ["GBP", "EUR"])
@pytest.mark.parametrize("target", ["USD"])
def test_rate_request(source: str, target: str) -> None:
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
