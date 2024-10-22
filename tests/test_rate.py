import pytest

from wisest.rate import Rate
from wisest.rate import RateHistoryRequest
from wisest.rate import Resolution
from wisest.rate import Unit
from wisest.rate import query_rate


@pytest.mark.parametrize("source", ["GBP", "EUR"])
@pytest.mark.parametrize("target", ["USD"])
def test_query_rate(source: str, target: str) -> None:
    rate = query_rate(source=source, target=target)

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

    for rate in rates:
        assert isinstance(rate, Rate)
        assert rate.source == source
        assert rate.target == target
