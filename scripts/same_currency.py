from __future__ import annotations

import click
from tqdm import tqdm

from wise import print_costs
from wise import query_price
from wise import query_rate


@click.command()
@click.option("-i", "--pay-in-method", type=click.STRING, default="VISA_CREDIT")
@click.option("-o", "--pay-out-method", type=click.STRING, default="BALANCE")
@click.option("--price-set-id", type=click.INT, default=None)
def main(
    pay_in_method: str,
    pay_out_method: str,
    price_set_id: int | None,
) -> None:
    currencies = [
        # "AED",
        "AUD",
        # "BGN",
        # "BRL",
        # "CAD",
        "CHF",
        # "CZK",
        # "DKK",
        "EUR",
        "GBP",
        # "HKD",
        "HUF",
        # "IDR",
        # "ILS",
        # "INR",
        # "JPY",
        # "MYR",
        # "NOK",
        "NZD",
        # "PHP",
        # "PLN",
        # "RON",
        # "SEK",
        "SGD",
        # "UAH",
        "USD",
    ]

    prices = [
        query_price(
            source_currency=currency,
            target_amount=1000 / query_rate(source=currency, target="USD").value,
            target_currency=currency,
            pay_in_method=pay_in_method,
            pay_out_method=pay_out_method,
            price_set_id=price_set_id,
        )
        for currency in tqdm(currencies)
    ]
    prices = sorted(prices, key=lambda x: x.variable_fee_percent)

    if price_set_id is not None:
        print(f"price_set_id: {price_set_id}")
    print_costs(prices)


if __name__ == "__main__":
    main()
