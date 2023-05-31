from wise.cost import Cost
from wise.payment import Payment
from typing import List


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

    costs: List[Cost] = []
    for source_currency in source_currencies:
        payment = Payment().pay_with(source_currency).add(1000, 'USD')
        cost = Cost(payment)
        costs.append(cost)

    # sort by total fee rate
    for cost in sorted(costs, key=lambda x: x.get_total_fee_rate()):
        print(cost)


if __name__ == '__main__':
    main()
