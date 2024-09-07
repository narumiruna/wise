from __future__ import annotations

from tabulate import tabulate

from .price import Price
from .rate import query_rate


def print_costs(prices: list[Price], card_fee_percent: float = 1.5, reward_rate: float = 0.1) -> None:
    table = []
    for price in prices:
        card_fee = price.source_amount * card_fee_percent / 100
        wise_fee_percent = 100 * price.total / price.source_amount
        fee = card_fee + price.total
        fee_percent = 100 * fee / (price.source_amount + card_fee)
        cost_per_mile = fee / (price.source_amount * reward_rate)

        table.append(
            [
                f"{price.price_set_id}",
                f"{price.source_amount:.2f} {price.source_currency}",
                f"{price.target_amount:.2f} {price.target_currency}",
                # f"{price.pay_in_method}",
                # f"{price.pay_out_method}",
                f"{price.mid_rate:.4f}",
                f"{price.total:.2f} {price.source_currency} ({wise_fee_percent:.2f}%)",
                f"{fee:.2f} {price.source_currency} ({fee_percent:.2f}%)",
                f"{cost_per_mile:.4f}",
            ]
        )

    print(
        tabulate(
            table,
            headers=[
                "Price Set ID",
                "Source",
                "Target",
                # "Pay In Method",
                # "Pay Out Method",
                "Mid Rate",
                "Wise Fee",
                "Total Fee",
                "Cost per Mile",
            ],
            tablefmt="rounded_grid",
            stralign="right",
        )
    )


def print_cash_back_costs(
    prices: list[Price], card_fee_percent: float = 1.5, cash_back_percent: float = 3.0, quote_currency: str = "TWD"
) -> None:
    table = []
    for price in prices:
        rate = query_rate(price.source_currency, quote_currency).value

        card_fee = price.source_amount * card_fee_percent / 100
        cash_back = price.source_amount * cash_back_percent / 100
        wise_fee_percent = 100 * price.total / price.source_amount
        fee = card_fee + price.total - cash_back
        fee_percent = 100 * fee / (price.source_amount + card_fee)

        table.append(
            [
                f"{price.price_set_id}",
                f"{price.source_amount:.2f} {price.source_currency}",
                f"{price.target_amount:.2f} {price.target_currency}",
                # f"{price.pay_in_method}",
                # f"{price.pay_out_method}",
                f"{price.mid_rate:.4f}",
                f"{card_fee*rate:.2f} {quote_currency} ({card_fee_percent:.2f}%)",
                f"{cash_back*rate:.2f} {quote_currency} ({cash_back_percent:.2f}%)",
                f"{price.total*rate:.2f} {quote_currency} ({wise_fee_percent:.2f}%)",
                f"{fee*rate:.2f} {quote_currency} ({fee_percent:.2f}%)",
            ]
        )

    print(
        tabulate(
            table,
            headers=[
                "Price Set ID",
                "Source",
                "Target",
                # "Pay In Method",
                # "Pay Out Method",
                "Mid Rate",
                "Card Fee",
                "Cash Back",
                "Wise Fee",
                "Total Fee",
            ],
            tablefmt="rounded_grid",
            stralign="right",
        )
    )
