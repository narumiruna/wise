from typing import List

import requests
from pydantic import BaseModel
from pydantic import Field


class Currency(BaseModel):
    code: str
    symbol: str
    name: str
    country_keywords: list[str] = Field(alias="countryKeywords")
    supports_decimals: bool = Field(alias="supportsDecimals")


def query_currencies() -> List[Currency]:
    url = "https://wise.com/gateway/v1/currencies"

    resp = requests.get(url)

    return [Currency(**c) for c in resp.json()]
