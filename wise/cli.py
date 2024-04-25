from itertools import product

import click
from tqdm import tqdm

from .price import Price
from .price import query_price


def print_cost(price: Price, card_fee_percent: float = 1.5, reward_rate: float = 0.1) -> None:
    card_fee = price.source_amount * card_fee_percent / 100
    wise_fee_percent = 100 * price.total / price.source_amount
    fee = card_fee + price.total
    fee_percent = 100 * fee / (price.source_amount + card_fee)
    cost_per_mile = fee / (price.source_amount * reward_rate)
    print(
        f"Add {price.target_amount:.2f} { price.target_currency}"
        f", pay {price.source_amount:.2f} {price.source_currency}"
        f", wise fee: {price.total:.2f} {price.source_currency} ({wise_fee_percent:.2f}%)"
        f", total fee: {fee:.2f} {price.source_currency} ({fee_percent:.2f}%)"
        f", cost per mile: {cost_per_mile:.4f}"
    )


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

    prices = [
        query_price(
            source_currency=source,
            target_amount=float(amount),
            target_currency=target,
            pay_in_method=pay_in_method,
            pay_out_method=pay_out_method,
        )
        for source, amount, target in tqdm(list(product(sources, amounts, targets)))
    ]

    # sort by total fee rate
    prices = sorted(prices, key=lambda p: p.variable_fee_percent)

    # print costs
    for price in prices:
        print_cost(price)
