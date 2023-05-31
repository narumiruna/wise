from typing import List

from .price import Price


def find_price(prices: List[Price], pay_in_method: str = 'BANK_TRANSFER', pay_out_method: str = 'BALANCE') -> Price:
    for price in prices:
        if price.payInMethod == pay_in_method.upper() and price.payOutMethod == pay_out_method.upper():
            return price

    raise ValueError(f'Price not found for pay_in_method={pay_in_method} and pay_out_method={pay_out_method}')
