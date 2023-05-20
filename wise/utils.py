from typing import List

from .wise_rate import Price


def get_bank_transfer_in_balance_out(prices: List[Price]):
    for price in prices:
        if price.payInMethod == 'BANK_TRANSFER' and price.payOutMethod == 'BALANCE':
            return price
    return None
