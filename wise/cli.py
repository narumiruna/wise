import click
from tqdm import tqdm

from .cost import Cost
from .price import get_price


@click.group()
def cli():
    pass


@cli.command()
@click.option("--target-amount", type=click.FLOAT, default=1000)
@click.option("--target-currency", type=click.STRING, default="USD")
def list(target_amount: str, target_currency: str) -> None:
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

    costs = []
    for source_currency in tqdm(source_currencies):
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


@cli.command()
@click.argument("source-currency", type=click.STRING)
@click.argument("target-amount", type=click.FLOAT)
@click.argument("target-currency", type=click.STRING)
def add(
    source_currency: str,
    target_amount: float,
    target_currency: str,
) -> None:
    price = get_price(
        source_currency=source_currency,
        target_amount=target_amount,
        target_currency=target_currency,
    )
    cost = Cost(price)
    print(cost)


@cli.command()
@click.argument("source_amount", type=click.FLOAT)
@click.argument("source_currency", type=click.STRING)
@click.argument("target_amount", type=click.FLOAT)
@click.argument("target_currency", type=click.STRING)
def calc(
    source_amount: float,
    source_currency: str,
    target_amount: float,
    target_currency: str,
):
    price = get_price(
        source_currency=source_currency,
        target_amount=target_amount,
        target_currency=target_currency,
    )
    price.update_source_amount(source_amount)

    cost = Cost(price)
    print(cost)
