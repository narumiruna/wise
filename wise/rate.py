from datetime import datetime
from enum import Enum
from typing import List

import requests
from pydantic import BaseModel
from pydantic import Field
from requests.utils import default_headers

DEFAULT_TIMEOUT = 10


def parse_datetime(x: int) -> datetime:
    return datetime.fromtimestamp(x // 1000)


# {"source":"EUR","target":"USD","value":1.05425,"time":1697653800557}
class Rate(BaseModel):
    source: str
    target: str
    value: float
    time: datetime = Field(default_factory=parse_datetime)


class Resolution(str, Enum):
    HOURLY = "hourly"
    DAILY = "daily"


class Unit(str, Enum):
    DAY = "day"
    MONTH = "month"
    YEAR = "year"


class RateRequest(BaseModel):
    source: str
    target: str

    def do(self) -> "Rate":
        resp = requests.get(
            "https://wise.com/rates/live",
            params=self.model_dump(),
            headers=default_headers(),
            timeout=DEFAULT_TIMEOUT,
        )
        return Rate(**resp.json())


# https://wise.com/rates/history?source=EUR&target=USD&length=10&resolution=daily&unit=day
class RateHistoryRequest(BaseModel):
    source: str
    target: str
    length: int
    resolution: Resolution
    unit: Unit

    def do(self) -> List["Rate"]:
        resp = requests.get(
            url="https://wise.com/rates/history",
            params=self.model_dump(),
            headers=default_headers(),
            timeout=DEFAULT_TIMEOUT,
        )

        return [Rate(**r) for r in resp.json()]


def query_rate(source: str, target: str) -> Rate:
    return RateRequest(source=source, target=target).do()


def query_rate_history(source: str, target: str, length: int, resolution: str, unit: str) -> List[Rate]:
    return RateHistoryRequest(source=source, target=target, length=length, resolution=resolution, unit=unit).do()
