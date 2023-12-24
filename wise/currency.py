from typing import List

import requests
from pydantic import BaseModel
from pydantic import Field
from requests.utils import default_headers

DEFAULT_TIMEOUT = 10


class CurrencyRequest(BaseModel):
    def do(self) -> List["Currency"]:
        resp = requests.get(
            url="https://wise.com/gateway/v1/currencies",
            headers=default_headers(),
            timeout=DEFAULT_TIMEOUT,
        )
        return [Currency(**c) for c in resp.json()]


class Currency(BaseModel):
    code: str
    symbol: str
    name: str
    country_keywords: list[str] = Field(alias="countryKeywords")
    supports_decimals: bool = Field(alias="supportsDecimals")


def query_currency() -> List[Currency]:
    return CurrencyRequest().do()
