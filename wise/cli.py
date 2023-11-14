from itertools import product

import click
from tqdm import tqdm

from .cost import get_cost

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
@click.argument("source-currency", type=click.STRING)
@click.argument("target-amount", type=click.STRING)
@click.argument("target-currency", type=click.STRING)
def cli(
    source_currency: str,
    target_amount: str,
    target_currency: str,
):
    sources = source_currency.split(",")
    amounts = [float(x) for x in target_amount.split(",")]
    targets = target_currency.split(",")

    costs = [
        get_cost(source, amount, target)
        for source, amount, target in tqdm(list(product(sources, amounts, targets)))
    ]

    # sort by total fee rate
    costs = sorted(costs, key=lambda x: x.price.total)

    # print costs
    for cost in costs:
        print(cost)
