from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from wisest import query_price
from wisest.cost import format_cash_back_costs
from wisest.method import PayInMethod
from wisest.method import PayOutMethod


def main(
    pay_in_method: Annotated[PayInMethod, typer.Option("-i", "--pay-in-method")] = PayInMethod.INTERNATIONAL_CREDIT,
    pay_out_method: Annotated[PayOutMethod, typer.Option("-o", "--pay-out-method")] = PayOutMethod.BALANCE,
    price_set_id: int | None = None,
    output_file: Annotated[str, typer.Option("--output-file")] = "add_usd.txt",
) -> None:
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
            pay_in_method=pay_in_method,
            pay_out_method=pay_out_method,
            price_set_id=price_set_id,
        )
        for currency in currencies
    ]
    prices = sorted(prices, key=lambda p: p.variable_fee_percent)

    if price_set_id is not None:
        print(f"price_set_id: {price_set_id}")

    result = format_cash_back_costs(prices)
    print(result)

    with Path(output_file).open("w") as fp:
        fp.write(
            "\n".join(
                [
                    f"Pay in Method: {pay_in_method.name}",
                    f"Pay out Method: {pay_out_method.name}",
                    result,
                ]
            )
        )


if __name__ == "__main__":
    typer.run(main)
