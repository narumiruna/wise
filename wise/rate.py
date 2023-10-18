from datetime import datetime

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


def get_rate(source: str, target: str) -> Rate:
    url = "https://wise.com/rates/live"

    resp = requests.get(url=url, params=dict(source=source, target=target))

    return Rate(**resp.json())
