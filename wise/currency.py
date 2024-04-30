from __future__ import annotations

from pydantic import BaseModel
from pydantic import Field

from .request import get


class CurrencyRequest(BaseModel):
    def do(self) -> list[Currency]:
        resp = get(
            url="https://wise.com/gateway/v1/currencies",
        )
        resp.raise_for_status()
        return [Currency.model_validate(data) for data in resp.json()]


class Currency(BaseModel):
    code: str
    symbol: str
    name: str
    country_keywords: list[str] = Field(alias="countryKeywords")
    supports_decimals: bool = Field(alias="supportsDecimals")
