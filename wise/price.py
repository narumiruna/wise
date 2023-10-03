from typing import List

import requests
from pydantic import BaseModel
from pydantic import parse_obj_as
from requests.utils import default_headers


class Price(BaseModel):
    priceSetId: int
    sourceAmount: float
    targetAmount: float
    payInMethod: str
    payOutMethod: str
    sourceCcy: str
    targetCcy: str
    total: float
    variableFee: float
    variableFeePercent: float
    swiftPayoutFlatFee: float
    flatFee: float
    midRate: float
    ecbRate: float
    ecbRateTimestamp: int
    ecbMarkupPercent: float
    additionalFeeDetails: dict

    @property
    def target_amount(self) -> float:
        return self.targetAmount

    @property
    def target_currency(self) -> str:
        return self.targetCcy

    @property
    def source_amount(self) -> float:
        return self.sourceAmount

    @property
    def source_currency(self) -> str:
        return self.sourceCcy


def get_price(
    source_amount: float = None,
    source_currency: str = None,
    target_amount: float = None,
    target_currency: str = None,
    pay_in_method: str = "VISA_CREDIT",
    pay_out_method: str = "BALANCE",
) -> Price:
    return find_price(
        get_prices(
            source_amount=source_amount,
            source_currency=source_currency,
            target_amount=target_amount,
            target_currency=target_currency,
        ),
        pay_in_method=pay_in_method,
        pay_out_method=pay_out_method,
    )


def get_prices(
    source_amount: float = None,
    source_currency: str = None,
    target_amount: float = None,
    target_currency: str = None,
    profile_id: str = None,
    profile_country: str = "TW",
    profile_type: str = "PERSONAL",
    markers: str = "FCF_PRICING",
) -> List[Price]:
    url = "http://wise.com/gateway/v1/price"

    params = dict(
        sourceCurrency=source_currency,
        targetCurrency=target_currency,
        profileCountry=profile_country,
        profileType=profile_type,
        markers=markers,
    )
    if source_amount is not None:
        params["sourceAmount"] = source_amount

    if target_amount is not None:
        params["targetAmount"] = target_amount

    if profile_id is not None:
        params["profileId"] = profile_id

    resp = requests.get(url=url, params=params, headers=default_headers())

    return parse_obj_as(List[Price], resp.json())


def find_price(
    prices: List[Price],
    pay_in_method: str = "VISA_CREDIT",
    pay_out_method: str = "BALANCE",
) -> Price:
    for price in prices:
        if (
            price.payInMethod == pay_in_method.upper()
            and price.payOutMethod == pay_out_method.upper()
        ):
            return price

    raise ValueError(
        f"Price not found for pay_in_method={pay_in_method} and pay_out_method={pay_out_method}"
    )
