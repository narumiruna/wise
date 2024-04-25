from .price import Price


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
