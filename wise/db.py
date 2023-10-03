import os

import influxdb_client
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

from .cost import Cost

DEFAULT_INFLUXDB_ORG = "narumi"
DEFAULT_INFLUXDB_URL = "http://127.0.0.1:8086"


class CostWriter:
    def __init__(self, client: InfluxDBClient, bucket: str):
        self.client = client
        self.bucket = bucket

        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def write(self, cost: Cost):
        points = []

        points.append(self.get_cost_point(cost))

        self.write_api.write(bucket=self.bucket, org=self.client.org, record=points)

    def get_cost_point(self, cost: Cost) -> Point:
        point = Point("cost")
        point.tag("source_currency", cost.source_currency)
        point.tag("target_currency", "USD")
        point.tag("target_amount", cost.target_amount)

        point.field("wise_fee", cost.wise_fee)
        point.field("card_fee", cost.card_fee)
        point.field("total_fee", cost.total_fee)
        point.field("total_fee_rate", cost.total_fee_rate)
        point.field("miles", cost.miles)
        point.field("amount", cost.source_amount)
        point.field("total_amount", cost.total_amount)
        point.field("source_amount", cost.source_amount)
        point.field("mile_price", cost.mile_price)
        return point

    @classmethod
    def from_env(cls, bucket: str = "wise"):
        load_dotenv(find_dotenv())

        url = os.environ.get("INFLUXDB_URL", DEFAULT_INFLUXDB_URL)
        token = os.environ.get("INFLUXDB_TOKEN")
        org = os.environ.get("INFLUXDB_ORG", DEFAULT_INFLUXDB_ORG)

        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        return cls(client, bucket=bucket)
