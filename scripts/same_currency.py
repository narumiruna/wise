from typing import List

from tqdm import tqdm

from wise import get_cost
from wise import query_rate
from wise.cost import Cost


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
        "PLN",
        "RON",
        "SEK",
        "SGD",
        "UAH",
        "USD",
    ]

    costs: List[Cost] = []
    for currency in tqdm(currencies):
        rate = query_rate(currency, "USD")
        cost = get_cost(currency, 1000 / rate.value, currency)
        costs.append(cost)

    costs = sorted(costs, key=lambda x: x.price.variable_fee_percent)

    for cost in costs:
        print(cost)


if __name__ == "__main__":
    main()
