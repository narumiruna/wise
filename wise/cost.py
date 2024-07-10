from __future__ import annotations

from tabulate import tabulate

from .price import Price


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
                f"{price.source_amount:.2f} {price.source_currency}",
                f"{price.target_amount:.2f} {price.target_currency}",
                f"{price.total:.2f} {price.source_currency} ({wise_fee_percent:.2f}%)",
                f"{fee:.2f} {price.source_currency} ({fee_percent:.2f}%)",
                f"{cost_per_mile:.4f}",
            ]
        )

    print(
        tabulate(
            table,
            headers=[
                "Source",
                "Target",
                "Wise Fee",
                "Total Fee",
                "Cost per Mile",
            ],
            tablefmt="rounded_grid",
            stralign="right",
        )
    )
