import click
from tqdm import tqdm

from wise import print_costs
from wise import query_price


@click.command()
@click.option("--new", is_flag=True, type=click.BOOL, help="New price set ID")
def main(new: bool) -> None:
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
            price_set_id=2593 if new else 2586,
        )
        for currency in tqdm(currencies)
    ]
    prices = sorted(prices, key=lambda p: p.variable_fee_percent)

    print_costs(prices)


if __name__ == "__main__":
    main()
