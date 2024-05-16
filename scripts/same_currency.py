from tqdm import tqdm

from wise import print_costs
from wise import query_price
from wise import query_rate


def main() -> None:
    currencies = [
        "AED",
        "AUD",
        "BGN",
        "BRL",
        "CAD",
        "CHF",
        "CZK",
        "DKK",
        "EUR",
        "GBP",
        "HKD",
        "HUF",
        "IDR",
        "ILS",
        "INR",
        "JPY",
        "MYR",
        "NOK",
        "NZD",
        "PLN",
        "RON",
        "SEK",
        "SGD",
        "UAH",
        "USD",
    ]

    prices = [
        query_price(
            source_currency=currency,
            target_amount=1000 / query_rate(source=currency, target="USD").value,
            target_currency=currency,
        )
        for currency in tqdm(currencies)
    ]
    prices = sorted(prices, key=lambda x: x.variable_fee_percent)

    print_costs(prices)


if __name__ == "__main__":
    main()
