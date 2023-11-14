from wise import query_rate
from wise import query_rate_history


def test_get_rate():
    rate = query_rate(source="EUR", target="USD")

    assert rate.source == "EUR"
    assert rate.target == "USD"


def test_get_rate_history():
    rates = query_rate_history(
        source="EUR", target="USD", length=10, resolution="daily", unit="day"
    )

    assert len(rates) == 10
    assert rates[0].source == "EUR"
    assert rates[0].target == "USD"
