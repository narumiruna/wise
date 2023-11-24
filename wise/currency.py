from typing import List

import requests
from pydantic import BaseModel
from pydantic import Field


class CurrencyRequest(BaseModel):
    def do(self) -> List["Currency"]:
        resp = requests.get(url="https://wise.com/gateway/v1/currencies")
        return [Currency(**c) for c in resp.json()]


class Currency(BaseModel):
    code: str
    symbol: str
    name: str
    country_keywords: list[str] = Field(alias="countryKeywords")
    supports_decimals: bool = Field(alias="supportsDecimals")


def query_currency() -> List[Currency]:
    return CurrencyRequest().do()
