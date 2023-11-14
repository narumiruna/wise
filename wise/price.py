from typing import List

import requests
from pydantic import BaseModel
from pydantic import Field
from requests.utils import default_headers


class Price(BaseModel):
    price_set_id: int = Field(None, alias="priceSetId")
    source_amount: float = Field(None, alias="sourceAmount")
    target_amount: float = Field(None, alias="targetAmount")
    pay_in_method: str = Field(None, alias="payInMethod")
    pay_out_method: str = Field(None, alias="payOutMethod")
    source_currency: str = Field(None, alias="sourceCcy")
    target_currency: str = Field(None, alias="targetCcy")
    total: float
    variable_fee: float = Field(None, alias="variableFee")
    variable_fee_percent: float = Field(None, alias="variableFeePercent")
    swift_payout_flat_fee: float = Field(None, alias="swiftPayoutFlatFee")
    flat_fee: float = Field(None, alias="flatFee")
    mid_rate: float = Field(None, alias="midRate")
    ecb_rate: float = Field(None, alias="ecbRate")
    ecb_rate_timestamp: int = Field(None, alias="ecbRateTimestamp")
    ecb_markup_percent: float = Field(None, alias="ecbMarkupPercent")
    additional_fee_details: dict = Field(None, alias="additionalFeeDetails")


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
    profile_country: str = None,
    profile_type: str = None,
    markers: str = None,
) -> List[Price]:
    # https://wise.com/gb/pricing/receive
    # https://wise.com/gb/pricing/send-money
    url = "http://wise.com/gateway/v1/price"

    params = dict(
        sourceAmount=source_amount,
        sourceCurrency=source_currency,
        targetAmount=target_amount,
        targetCurrency=target_currency,
        profileId=profile_id,
        profileCountry=profile_country,
        profileType=profile_type,
        markers=markers,
    )

    resp = requests.get(url=url, params=params, headers=default_headers())

    return [Price(**data) for data in resp.json()]


def find_price(
    prices: List[Price],
    pay_in_method: str = "VISA_CREDIT",
    pay_out_method: str = "BALANCE",
) -> Price:
    for price in prices:
        if (
            price.pay_in_method == pay_in_method.upper()
            and price.pay_out_method == pay_out_method.upper()
        ):
            return price

    raise ValueError(
        f"Price not found for pay_in_method={pay_in_method} and pay_out_method={pay_out_method}"
    )
