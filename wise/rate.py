from datetime import datetime
from typing import List

import requests
from pydantic import BaseModel
from pydantic import field_validator


# {"source":"EUR","target":"USD","value":1.05425,"time":1697653800557}
class Rate(BaseModel):
    source: str
    target: str
    value: float
    time: int

    @field_validator("time")
    def to_datetime(x) -> datetime:
        return datetime.fromtimestamp(x // 1000)


def query_rate(source: str, target: str) -> Rate:
    # https://wise.com/tools/exchange-rate-alerts/
    # https://wise.com/rates/live?source=EUR&target=USD
    url = "https://wise.com/rates/live"

    resp = requests.get(url=url, params=dict(source=source, target=target))

    return Rate(**resp.json())


def query_rate_history(
    source: str, target: str, length: int, resolution: str, unit: str
) -> List[Rate]:
    if resolution not in ["hourly", "daily"]:
        raise ValueError("resolution must be hourly or daily")

    if unit not in ["day", "month", "year"]:
        raise ValueError("unit must be day, month or year")

    # https://wise.com/rates/history?source=EUR&target=USD&length=10&resolution=daily&unit=day
    url = "https://wise.com/rates/history"

    resp = requests.get(
        url=url,
        params=dict(
            source=source,
            target=target,
            length=length,
            resolution=resolution,
            unit=unit,
        ),
    )

    return [Rate(**r) for r in resp.json()]
