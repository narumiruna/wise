from typing import List

from dotenv import load_dotenv

from wise import Payment
from wise.cost import Cost


def main() -> None:
    target_amount = 1000
    target_currency = 'USD'

    source_currencies = [
        'AUD', 'BRL', 'CAD', 'CHF', 'CZK', 'DKK', 'EUR', 'GBP', 'HUF', 'IDR', 'INR', 'JPY', 'NOK', 'NZD', 'PLN', 'RON',
        'SEK', 'SGD', 'USD'
    ]

    costs: List[Cost] = []
    for source_currency in source_currencies:
        p = Payment().add(target_amount, target_currency).pay_with(source_currency)
        costs += [Cost(p)]

    costs = sorted(costs, key=lambda c: c.total_fee_rate)
    for cost in costs:
        print(cost)


if __name__ == "__main__":
    main()
