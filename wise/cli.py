from itertools import product

import click
from tqdm import tqdm

from .cost import print_costs
from .price import query_price


@click.command()
@click.argument("source-currency", type=click.STRING)
@click.argument("target-amount", type=click.STRING)
@click.argument("target-currency", type=click.STRING)
@click.option("-i", "--pay-in-method", type=click.STRING, default="GOOGLE_PAY")
@click.option("-o", "--pay-out-method", type=click.STRING, default="BALANCE")
@click.option("--new", is_flag=True, type=click.BOOL)
def cli(
    source_currency: str,
    target_amount: str,
    target_currency: str,
    pay_in_method: str,
    pay_out_method: str,
    new: bool,
) -> None:
    sources = source_currency.split(",")
    amounts = [float(x) for x in target_amount.split(",")]
    targets = target_currency.split(",")

    prices = [
        query_price(
            source_currency=source,
            target_amount=float(amount),
            target_currency=target,
            pay_in_method=pay_in_method,
            pay_out_method=pay_out_method,
            price_set_id=2593 if new else 2586,
        )
        for source, amount, target in tqdm(list(product(sources, amounts, targets)))
    ]

    # sort by total fee rate
    prices = sorted(prices, key=lambda p: p.variable_fee_percent)

    # print costs
    print_costs(prices)
