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
                # f"{price.price_set_id}",
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
                # "Price Set ID",
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
    prices: list[Price],
    card_fee_percent: float = 1.5,
    # reward_rate: float = 0.1,
    cash_back_percent: float = 3.0,
) -> None:
    table = []
    for price in prices:
        card_fee = price.source_amount * card_fee_percent / 100
        wise_fee_percent = 100 * price.total / price.source_amount
        fee = card_fee + price.total
        fee_percent = 100 * fee / (price.source_amount + card_fee)
        cash_back = price.source_amount * cash_back_percent / 100
        cost = fee - cash_back
        cost_percent = 100 * cost / price.source_amount
        # cost_per_mile = fee / (price.source_amount * reward_rate)

        table.append(
            [
                # f"{price.price_set_id}",
                f"{price.source_amount:.2f} {price.source_currency}",
                f"{price.target_amount:.2f} {price.target_currency}",
                f"{price.total:.2f} {price.source_currency} ({wise_fee_percent:.2f}%)",
                f"{fee:.2f} {price.source_currency} ({fee_percent:.2f}%)",
                f"{cash_back:.2f} {price.source_currency} ({cash_back_percent:.2f}%)",
                f"{cost:.2f} {price.source_currency} ({cost_percent:.2f}%)",
                # f"{cost_per_mile:.4f}",
            ]
        )

    print(
        tabulate(
            table,
            headers=[
                # "Price Set ID",
                "Source",
                "Target",
                "Wise Fee",
                "Total Fee",
                "Cash Back",
                "Cost",
                # "Cost per Mile",
            ],
            tablefmt="rounded_grid",
            stralign="right",
        )
    )
