from typing import List

import requests
from pydantic import parse_obj_as
from requests.utils import default_headers

from .price import Price


def get_wise_prices(source_amount: float = None,
                    source_currency: str = None,
                    target_amount: float = None,
                    target_currency: str = None,
                    profile_id: str = None,
                    profile_country: str = "TW",
                    profile_type: str = 'PERSONAL',
                    markers: str = 'FCF_PRICING') -> List[Price]:
    url = 'http://wise.com/gateway/v1/price'

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

    return parse_obj_as(List[Price], resp.json())
