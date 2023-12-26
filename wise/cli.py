from itertools import product

import click
from tqdm import tqdm

from .cost import get_cost


@click.command()
@click.argument("source-currency", type=click.STRING)
@click.argument("target-amount", type=click.STRING)
@click.argument("target-currency", type=click.STRING)
@click.option("-i", "--pay-in-method", type=click.STRING, default="VISA_CREDIT")
@click.option("-o", "--pay-out-method", type=click.STRING, default="BALANCE")
def cli(
    source_currency: str,
    target_amount: str,
    target_currency: str,
    pay_in_method: str,
    pay_out_method: str,
) -> None:
    sources = source_currency.split(",")
    amounts = [float(x) for x in target_amount.split(",")]
    targets = target_currency.split(",")

    costs = [
        get_cost(
            source,
            float(amount),
            target,
            pay_in_method=pay_in_method,
            pay_out_method=pay_out_method,
        )
        for source, amount, target in tqdm(list(product(sources, amounts, targets)))
    ]

    # sort by total fee rate
    costs = sorted(costs, key=lambda x: x.price.variable_fee_percent)

    # print costs
    for cost in costs:
        print(cost)
