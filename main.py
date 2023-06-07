from itertools import product
from typing import List

import click

from wise import SlackBot
from wise.cost import Cost
from wise.db import CostWriter
from wise.payment import Payment


@click.command()
@click.option('--write-cost', is_flag=True, default=False, help='Write cost to influxdb')
@click.option('--send-slack', is_flag=True, default=False, help='Send slack message')
def main(write_cost: bool, send_slack: bool):

    # 'BGN',  # google pay not supported
    source_currencies = [
        'AUD', 'BRL', 'CAD', 'CHF', 'CZK', 'DKK', 'EUR', 'GBP', 'HUF', 'IDR', 'INR', 'JPY', 'NOK', 'NZD', 'PLN', 'RON',
        'SEK', 'SGD', 'USD'
    ]

    amounts = [1000, 1500, 2000]

    writer = None
    if write_cost:
        writer = CostWriter.from_env()

    if send_slack:
        bot = SlackBot.from_env()

    costs: List[Cost] = []
    for source_currency, amount in product(source_currencies, amounts):
        payment = Payment().pay_with(source_currency).add(amount, 'USD')
        cost = Cost(payment)
        costs.append(cost)

        if writer is not None:
            writer.write(cost)

        if send_slack:
            bot.check(cost)

    # sort by total fee rate
    for cost in sorted(costs, key=lambda x: x.total_fee_rate):
        print(cost)


if __name__ == '__main__':
    main()
