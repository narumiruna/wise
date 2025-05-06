from __future__ import annotations

from itertools import product
from typing import Annotated

import typer

from .cost import print_cash_back_costs
from .method import PayInMethod
from .method import PayOutMethod
from .price import query_price


def _main(
    source_currency: str,
    target_amount: str,
    target_currency: str,
    pay_in_method: Annotated[PayInMethod, typer.Option("-i", "--pay-in-method")] = PayInMethod.GOOGLE_PAY,
    pay_out_method: Annotated[PayOutMethod, typer.Option("-o", "--pay-out-method")] = PayOutMethod.BALANCE,
    price_set_id: int | None = None,
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
            price_set_id=price_set_id,
        )
        for source, amount, target in list(product(sources, amounts, targets))
    ]

    # sort by total fee rate
    prices = sorted(prices, key=lambda p: p.variable_fee_percent)

    # print costs
    print_cash_back_costs(prices)


def main() -> None:
    typer.run(_main)
