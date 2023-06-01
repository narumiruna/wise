from itertools import product
from typing import List

from wise.cost import Cost
from wise.payment import Payment


def main():
    source_currencies = [
        'AUD',
        # 'BGN',  # google pay not supported
        'BRL',
        'CAD',
        'CHF',
        'CZK',
        'DKK',
        'EUR',
        'GBP',
        'HUF',
        'IDR',
        'INR',
        'JPY',
        'NOK',
        'NZD',
        'PLN',
        'RON',
        'SEK',
        'SGD',
        'USD',
    ]

    amounts = [1000, 1500, 2000]

    costs: List[Cost] = []
    for source_currency, amount in product(source_currencies, amounts):
        payment = Payment().pay_with(source_currency).add(amount, 'USD')
        cost = Cost(payment)
        costs.append(cost)

    # sort by total fee rate
    for cost in sorted(costs, key=lambda x: x.get_total_fee_rate()):
        print(cost)


if __name__ == '__main__':
    main()
