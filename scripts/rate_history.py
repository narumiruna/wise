from wise.rate import RateHistoryRequest
from wise.rate import Resolution
from wise.rate import Unit


def main() -> None:
    # Query USD/TWD exchange rate history for the past 2 months with daily resolution
    req = RateHistoryRequest(
        source="USD",
        target="TWD",
        length=2,
        resolution=Resolution.DAILY,
        unit=Unit.MONTH,
    )
    rates = req.do_sync()
    for rate in rates:
        print(rate)


if __name__ == "__main__":
    main()
