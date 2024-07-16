from __future__ import annotations

import click
from tqdm import tqdm

from wise import print_costs
from wise import query_price


@click.command()
@click.option("--price-set-id", type=click.INT, default=None)
def main(price_set_id: int | None) -> None:
    currencies = [
        "AED",
        "AUD",
        "BGN",
        "BRL",
        "CAD",
        "CHF",
        "CZK",
        "DKK",
        "EUR",
        "GBP",
        "HKD",
        "HUF",
        "IDR",
        "ILS",
        "INR",
        "JPY",
        "MYR",
        "NOK",
        "NZD",
        "PHP",
        "PLN",
        "RON",
        "SEK",
        "SGD",
        "UAH",
        "USD",
    ]

    prices = [
        query_price(
            source_currency=currency,
            target_amount=1000,
            target_currency="USD",
            price_set_id=price_set_id,
        )
        for currency in tqdm(currencies)
    ]
    prices = sorted(prices, key=lambda p: p.variable_fee_percent)

    if price_set_id is not None:
        print(f"price_set_id: {price_set_id}")
    print_costs(prices)


if __name__ == "__main__":
    main()
