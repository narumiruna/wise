from datetime import datetime

import cloudscraper


def visa_rate(amount: float = 1000, from_curr: str = 'TWD', to_curr: str = 'USD', fee: float = 0.0):
    url = 'https://www.visa.com.tw/cmsapi/fx/rates'

    params = dict(
        amount=amount,
        utcConvertedDate=datetime.now().strftime('%m%d%Y'),
        exchangedate=datetime.now().strftime('%m/%d/%Y'),
        fromCurr=from_curr,
        toCurr=to_curr,
        fee=fee,
    )

    resp = cloudscraper.create_scraper().get(url=url, params=params)

    return resp.json()
