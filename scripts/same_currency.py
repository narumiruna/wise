
from tqdm import tqdm

from wise import Cost
from wise import get_cost
from wise import query_rate


def get_costs(currencies: list[str]) -> list[Cost]:
    costs = []
    for currency in tqdm(currencies):
        rate = query_rate(currency, "USD")
        cost = get_cost(currency, 1000 / rate.value, currency)
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

    costs = get_costs(currencies)
    costs = sorted(costs, key=lambda x: x.price.variable_fee_percent)
    for cost in costs:
        print(cost)


if __name__ == "__main__":
    main()
