import pytest
from aiolimiter import AsyncLimiter

from wise.rate import Rate
from wise.rate import RateHistoryRequest
from wise.rate import RateRequest
from wise.rate import Resolution
from wise.rate import Unit
from wise.rate import query_rate


@pytest.mark.parametrize("source", ["GBP"])
@pytest.mark.parametrize("target", ["USD"])
def test_query_rate(source: str, target: str) -> None:
    rate = query_rate(source=source, target=target)

    assert isinstance(rate, Rate)
    assert rate.source == source
    assert rate.target == target


@pytest.mark.parametrize("source", ["GBP"])
@pytest.mark.parametrize("target", ["USD"])
def test_rate_request(source: str, target: str) -> None:
    rate = RateRequest(source=source, target=target).do_sync()

    assert isinstance(rate, Rate)
    assert rate.source == source
    assert rate.target == target


@pytest.mark.asyncio
@pytest.mark.parametrize("source", ["GBP"])
@pytest.mark.parametrize("target", ["USD"])
async def test_rate_request_async(source: str, target: str) -> None:
    async with AsyncLimiter(1, 0.05):
        rate = await RateRequest(source=source, target=target).do()

    assert isinstance(rate, Rate)
    assert rate.source == source
    assert rate.target == target


@pytest.mark.parametrize("source", ["EUR"])
@pytest.mark.parametrize("target", ["USD"])
def test_rate_history_request(source: str, target: str) -> None:
    length = 10

    rates = RateHistoryRequest(
        source=source,
        target=target,
        length=length,
        resolution=Resolution.DAILY,
        unit=Unit.DAY,
    ).do_sync()

    for rate in rates:
        assert isinstance(rate, Rate)
        assert rate.source == source
        assert rate.target == target


@pytest.mark.asyncio
@pytest.mark.parametrize("source", ["EUR"])
@pytest.mark.parametrize("target", ["USD"])
async def test_rate_history_request_async(source: str, target: str) -> None:
    length = 10
    async with AsyncLimiter(1, 0.05):
        rates = await RateHistoryRequest(
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
