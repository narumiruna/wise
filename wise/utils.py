from typing import List

from .price import Price


def get_bank_transfer_in_balance_out(prices: List[Price]) -> Price:
    for price in prices:
        if price.payInMethod == 'BANK_TRANSFER' and price.payOutMethod == 'BALANCE':
            return price

    raise ValueError('Bank transfer in balance out not found')
