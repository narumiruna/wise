from tqdm import tqdm

from wise import Price
from wise import RateRequest
from wise import print_cost
from wise import query_price


def get_prices(currencies: list[str]) -> list[Price]:
    costs = []
    for currency in tqdm(currencies):
        rate = RateRequest(source=currency, target="USD").do()
        cost = query_price(source_currency=currency, target_amount=1000 / rate.value, target_currency=currency)
        costs.append(cost)
    return costs


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

    prices = get_prices(currencies)
    prices = sorted(prices, key=lambda x: x.variable_fee_percent)
    for price in prices:
        print_cost(price)


if __name__ == "__main__":
    main()
