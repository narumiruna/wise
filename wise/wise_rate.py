import requests
from requests.utils import default_headers


def wise_rate(
    source_amount: float = None,
    source_currency: str = None,
    target_amount: float = None,
    target_currency: str = None,
    profile_id: str = None,
    profile_country: str = "US",
    profile_type: str = 'PERSONAL',
    markers: str = 'FCF_PRICING',
):
    url = 'https://wise.com/gateway/v1/price'

    params = dict(
        sourceCurrency=source_currency,
        targetCurrency=target_currency,
        profileCountry=profile_country,
        profileType=profile_type,
        markers=markers,
    )
    if source_amount is not None:
        params['sourceAmount'] = source_amount

    if target_amount is not None:
        params['targetAmount'] = target_amount

    if profile_id is not None:
        params['profileId'] = profile_id

    resp = requests.get(url=url, params=params, headers=default_headers())

    return resp.json()
