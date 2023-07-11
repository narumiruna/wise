from datetime import datetime
from typing import List

from markdown import Markdown
from telegraph import Telegraph

from .price import Price


def find_price(prices: List[Price], pay_in_method: str, pay_out_method: str = 'BALANCE') -> Price:
    for price in prices:
        if price.payInMethod == pay_in_method.upper() and price.payOutMethod == pay_out_method.upper():
            return price

    raise ValueError(f'Price not found for pay_in_method={pay_in_method} and pay_out_method={pay_out_method}')


def create_page(content: str = 'this is content'):
    telegraph = Telegraph()
    telegraph.create_account(short_name='Wise Bot')

    contents = [
        datetime.now().isoformat(),
        content,
    ]

    md = Markdown().set_output_format('html')
    resp = telegraph.create_page(
        title='Wise Fee',
        html_content=md.convert('\n\n'.join(contents)),
    )
    return resp