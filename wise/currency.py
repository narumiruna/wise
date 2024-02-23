from __future__ import annotations

import requests
from pydantic import BaseModel
from pydantic import Field
from requests.utils import default_headers

default_timeout = 10


class CurrencyRequest(BaseModel):
    def do(self) -> list[Currency]:
        resp = requests.get(
            url="https://wise.com/gateway/v1/currencies",
            headers=default_headers(),
            timeout=default_timeout,
        )
        return [Currency(**c) for c in resp.json()]


class Currency(BaseModel):
    code: str
    symbol: str
    name: str
    country_keywords: list[str] = Field(alias="countryKeywords")
    supports_decimals: bool = Field(alias="supportsDecimals")
