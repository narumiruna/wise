from typing import List
from typing import Optional

import requests
from pydantic import BaseModel
from pydantic import Field
from requests.utils import default_headers


class Price(BaseModel):
    price_set_id: int = Field(alias="priceSetId")
    source_amount: float = Field(alias="sourceAmount")
    target_amount: float = Field(alias="targetAmount")
    pay_in_method: str = Field(alias="payInMethod")
    pay_out_method: str = Field(alias="payOutMethod")
    source_currency: str = Field(alias="sourceCcy")
    target_currency: str = Field(alias="targetCcy")
    total: float
    variable_fee: float = Field(alias="variableFee")
    variable_fee_percent: float = Field(alias="variableFeePercent")
    swift_payout_flat_fee: float = Field(alias="swiftPayoutFlatFee")
    flat_fee: float = Field(alias="flatFee")
    mid_rate: float = Field(alias="midRate")
    ecb_rate: float = Field(alias="ecbRate")
    ecb_rate_timestamp: int = Field(alias="ecbRateTimestamp")
    ecb_markup_percent: float = Field(alias="ecbMarkupPercent")
    additional_fee_details: dict = Field(alias="additionalFeeDetails")


class PriceRequest(BaseModel):
    sourceAmount: Optional[float] = Field(None, alias="source_amount")
    sourceCurrency: Optional[str] = Field(None, alias="source_currency")
    targetAmount: Optional[float] = Field(None, alias="target_amount")
    targetCurrency: Optional[str] = Field(None, alias="target_currency")
    profileId: Optional[str] = Field(None, alias="profile_id")
    profileCountry: Optional[str] = Field(None, alias="profile_country")
    profileType: Optional[str] = Field(None, alias="profile_type")
    markers: Optional[str] = None

    def do(self) -> List[Price]:
        # https://wise.com/gb/pricing/receive
        # https://wise.com/gb/pricing/send-money

        resp = requests.get(
            url="http://wise.com/gateway/v1/price",
            params=self.model_dump(exclude_none=True),
            headers=default_headers(),
            timeout=10,
        )
        return [Price(**data) for data in resp.json()]


def query_price(
    source_amount: Optional[float] = None,
    source_currency: Optional[str] = None,
    target_amount: Optional[float] = None,
    target_currency: Optional[str] = None,
    profile_id: Optional[str] = None,
    profile_country: Optional[str] = None,
    profile_type: Optional[str] = None,
    markers: Optional[str] = None,
) -> List[Price]:
    return PriceRequest(
        source_amount=source_amount,
        source_currency=source_currency,
        target_amount=target_amount,
        target_currency=target_currency,
        profile_id=profile_id,
        profile_country=profile_country,
        profile_type=profile_type,
        markers=markers,
    ).do()


def find_price(
    prices: List[Price],
    pay_in_method: str = "VISA_CREDIT",
    pay_out_method: str = "BALANCE",
) -> Price:
    for price in prices:
        if price.pay_in_method == pay_in_method.upper() and price.pay_out_method == pay_out_method.upper():
            return price

    msg = f"Price not found for pay_in_method={pay_in_method} and pay_out_method={pay_out_method}"
    raise ValueError(msg)
