from typing import List

from tqdm import tqdm

from wise import Cost
from wise import get_cost


def main():
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

    costs: List[Cost] = []
    for currency in tqdm(currencies):
        cost = get_cost(currency, 1000, "USD")
        costs.append(cost)

    costs = sorted(costs, key=lambda x: x.price.variable_fee_percent)

    for cost in costs:
        print(cost)


if __name__ == "__main__":
    main()
