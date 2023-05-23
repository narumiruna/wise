from datetime import datetime

import cloudscraper
from pydantic import BaseModel
from retry import retry

# d = {
#     'originalValues': {
#         'fromCurrency': 'USD',
#         'fromCurrencyName': 'United States Dollar',
#         'toCurrency': 'TWD',
#         'toCurrencyName': 'New Taiwan Dollar',
#         'asOfDate': 1684595009,
#         'fromAmount': '1000',
#         'toAmountWithVisaRate': '30619',
#         'toAmountWithAdditionalFee': '30619',
#         'fxRateVisa': '30.619',
#         'fxRateWithAdditionalFee': '30.619',
#         'lastUpdatedVisaRate': 1684540259,
#         'benchmarks': []
#     },
#     'conversionAmountValue': '1000',
#     'conversionBankFee': '0.0',
#     'conversionInputDate': '05/20/2023',
#     'conversionFromCurrency': 'TWD',
#     'conversionToCurrency': 'USD',
#     'fromCurrencyName': 'United States Dollar',
#     'toCurrencyName': 'New Taiwan Dollar',
#     'convertedAmount': '30,619.000000',
#     'benchMarkAmount': '',
#     'fxRateWithAdditionalFee': '30.619',
#     'reverseAmount': '0.032659',
#     'disclaimerDate': 'May 20, 2023',
#     'status': 'success'
# }


class OriginalValues(BaseModel):
    fromCurrency: str
    fromCurrencyName: str
    toCurrency: str
    toCurrencyName: str
    asOfDate: int
    fromAmount: str
    toAmountWithVisaRate: str
    toAmountWithAdditionalFee: str
    fxRateVisa: str
    fxRateWithAdditionalFee: str
    lastUpdatedVisaRate: int
    benchmarks: list


class FxRate(BaseModel):
    originalValues: OriginalValues
    conversionAmountValue: str
    conversionBankFee: str
    conversionInputDate: str
    conversionFromCurrency: str
    conversionToCurrency: str
    fromCurrencyName: str
    toCurrencyName: str
    convertedAmount: str
    benchMarkAmount: str
    fxRateWithAdditionalFee: str
    reverseAmount: str
    disclaimerDate: str
    status: str


@retry(tries=100, delay=1)
def get_visa_fx_rate(amount: float = 1.0, from_curr: str = 'TWD', to_curr: str = 'USD', fee: float = 0.0) -> FxRate:
    url = 'http://www.visa.com.tw/cmsapi/fx/rates'

    params = dict(
        amount=amount,
        utcConvertedDate=datetime.now().strftime('%m%d%Y'),
        exchangedate=datetime.now().strftime('%m/%d/%Y'),
        fromCurr=from_curr,
        toCurr=to_curr,
        fee=fee,
    )

    scraper = cloudscraper.create_scraper()

    resp = scraper.get(url=url, params=params)

    with open('visa.html', 'wb') as f:
        f.write(resp.content)

    return FxRate.parse_obj(resp.json())
