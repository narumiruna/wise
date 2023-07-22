from itertools import product
from typing import List

import click
from dotenv import load_dotenv

from wise.mile_cost import MileCost
from wise.payment import Payment
from wise.telegram import TelegramBot
from wise.utils import create_page


@click.command()
@click.option('--threshold', type=click.FLOAT, default=0.02, help='Threshold for telegram message')
def main(threshold: float):
    load_dotenv()

    # 'BGN',  # google pay not supported
    source_currencies = [
        'AUD',
        # 'BRL',
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

    costs: List[MileCost] = []
    for source_currency, amount in product(source_currencies, amounts):
        payment = Payment().pay_with(source_currency).add(amount, 'USD')
        cost = MileCost(payment)
        costs.append(cost)

    # sort by total fee rate
    costs = sorted(costs, key=lambda x: x.total_fee_rate)

    # print costs
    for cost in costs:
        print(cost)

    low_costs = [str(cost) for cost in costs if cost.total_fee_rate <= threshold]
    if low_costs:
        s = '\n\n'.join(low_costs)
        TelegramBot.from_env().send(create_page(s)['url'])


if __name__ == '__main__':
    main()
