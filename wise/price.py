from __future__ import annotations

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator

from .request import get


class Price(BaseModel):
    price_set_id: int = Field(validation_alias="priceSetId")
    source_amount: float = Field(validation_alias="sourceAmount")
    target_amount: float = Field(validation_alias="targetAmount")
    pay_in_method: str = Field(validation_alias="payInMethod")
    pay_out_method: str = Field(validation_alias="payOutMethod")
    source_currency: str = Field(validation_alias="sourceCcy")
    target_currency: str = Field(validation_alias="targetCcy")
    total: float
    variable_fee: float = Field(validation_alias="variableFee")
    variable_fee_percent: float = Field(validation_alias="variableFeePercent")
    swift_payout_flat_fee: float = Field(validation_alias="swiftPayoutFlatFee")
    flat_fee: float = Field(validation_alias="flatFee")
    mid_rate: float = Field(validation_alias="midRate")
    ecb_rate: float = Field(validation_alias="ecbRate")
    ecb_rate_timestamp: int = Field(validation_alias="ecbRateTimestamp")
    ecb_markup_percent: float = Field(validation_alias="ecbMarkupPercent")
    additional_fee_details: dict = Field(validation_alias="additionalFeeDetails")


class PriceRequest(BaseModel):
    source_amount: float | None = Field(default=None, serialization_alias="sourceAmount")
    source_currency: str | None = Field(default=None, serialization_alias="sourceCurrency")
    target_amount: float | None = Field(default=None, serialization_alias="targetAmount")
    target_currency: str | None = Field(default=None, serialization_alias="targetCurrency")
    profile_id: str | None = Field(default=None, serialization_alias="profileId")
    profile_country: str | None = Field(default=None, serialization_alias="profileCountry")
    profile_type: str | None = Field(default=None, serialization_alias="profileType")
    markers: str | None = None
    price_set_id: int | None = Field(default=None, serialization_alias="priceSetId")

    @field_validator("source_currency", "target_currency")
    @classmethod
    def upper(cls, s: str) -> str:
        return s.upper()

    def do(self) -> list[Price]:
        # https://wise.com/gb/pricing/receive
        # https://wise.com/gb/pricing/send-money
        # https://wise.com/price-change/borderless-add

        resp = get(
            url="https://wise.com/gateway/v1/price",
            params=self.model_dump(exclude_none=True, by_alias=True),
        )
        resp.raise_for_status()
        return [Price.model_validate(data) for data in resp.json()]


def find_price(
    prices: list[Price],
    pay_in_method: str = "GOOGLE_PAY",
    pay_out_method: str = "BALANCE",
) -> Price:
    for price in prices:
        if price.pay_in_method == pay_in_method.upper() and price.pay_out_method == pay_out_method.upper():
            return price

    msg = f"Price not found for pay_in_method={pay_in_method} and pay_out_method={pay_out_method}"
    raise ValueError(msg)


def query_price(
    source_amount: float | None = None,
    source_currency: str | None = None,
    target_amount: float | None = None,
    target_currency: str | None = None,
    pay_in_method: str = "GOOGLE_PAY",
    pay_out_method: str = "BALANCE",
    price_set_id: int = 2586,
) -> Price:
    prices = PriceRequest(
        source_amount=source_amount,
        source_currency=source_currency,
        target_amount=target_amount,
        target_currency=target_currency,
        price_set_id=price_set_id,
    ).do()
    price = find_price(
        prices,
        pay_in_method=pay_in_method,
        pay_out_method=pay_out_method,
    )
    return price
