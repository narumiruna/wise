from itertools import product

import click
from tqdm import tqdm

from .cost import Cost
from .price import get_price

# 'BGN' not supported by google pay
# 'BRL' not supported by yahoo finance
source_currencies = [
    "AUD",
    "CAD",
    "CHF",
    "CZK",
    "DKK",
    "EUR",
    "GBP",
    "HUF",
    "IDR",
    "INR",
    "JPY",
    "NOK",
    "NZD",
    "PLN",
    "RON",
    "SEK",
    "SGD",
    "USD",
]


@click.command()
@click.argument("source-currencies", type=click.STRING)
@click.argument("target-amounts", type=click.STRING)
@click.argument("target-currencies", type=click.STRING)
def cli(
    source_currencies: str,
    target_amounts: str,
    target_currencies: str,
):
    source_currencies = source_currencies.split(",")
    target_amounts = [float(x) for x in target_amounts.split(",")]
    target_currencies = target_currencies.split(",")

    costs = []
    for source_currency, target_amount, target_currency in tqdm(
        list(product(source_currencies, target_amounts, target_currencies))
    ):
        price = get_price(
            source_currency=source_currency,
            target_amount=target_amount,
            target_currency=target_currency,
        )
        cost = Cost(price)
        costs.append(cost)

    # sort by total fee rate
    costs = sorted(costs, key=lambda x: x.total_fee_rate)

    # print costs
    for cost in costs:
        print(cost)
