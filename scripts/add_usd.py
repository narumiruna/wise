from tqdm import tqdm

from wise import print_cost
from wise import query_price


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
        "PHP",
        "PLN",
        "RON",
        "SEK",
        "SGD",
        "UAH",
        "USD",
    ]

    prices = [
        query_price(source_currency=currency, target_amount=1000, target_currency="USD")
        for currency in tqdm(currencies)
    ]
    prices = sorted(prices, key=lambda p: p.variable_fee_percent)

    for price in prices:
        print_cost(price)


if __name__ == "__main__":
    main()
