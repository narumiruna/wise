import os
from typing import List

import influxdb_client
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

from .mile_cost import MileCost

DEFAULT_INFLUXDB_ORG = 'narumi'
DEFAULT_INFLUXDB_URL = 'http://127.0.0.1:8086'


class CostWriter:

    def __init__(self, client: InfluxDBClient, bucket: str):
        self.client = client
        self.bucket = bucket

        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def write(self, cost: MileCost):
        points = []

        points.append(self.get_cost_point(cost))
        points.extend(self.get_fx_rate_points(cost))

        self.write_api.write(bucket=self.bucket, org=self.client.org, record=points)

    def get_cost_point(self, cost: MileCost) -> Point:
        point = Point('cost')
        point.tag('source_currency', cost.source_currency)
        point.tag('target_currency', 'USD')
        point.tag('target_amount', cost.target_amount)

        point.field('wise_fee', cost.wise_fee)
        point.field('card_fee', cost.card_fee)
        point.field('total_fee', cost.total_fee)
        point.field('total_fee_rate', cost.total_fee_rate)
        point.field('miles', cost.miles)
        point.field('amount', cost.amount)
        point.field('total_amount', cost.total_amount)
        point.field('source_amount', cost.source_amount)
        point.field('mile_price', cost.mile_price)
        return point

    def get_fx_rate_points(self, cost: MileCost) -> List[Point]:
        base_currencies = [cost.source_currency, cost.target_currency]

        points = []
        for base_currency in base_currencies:
            point = Point('fx_rate')
            point.tag('base_currency', base_currency)
            point.tag('quote_currency', cost.quote_currency)
            point.field('rate', cost.get_fx_rate(base_currency, cost.quote_currency))
            points.append(point)

        return points

    @classmethod
    def from_env(cls, bucket: str = 'wise'):
        load_dotenv()

        url = os.environ.get('INFLUXDB_URL', DEFAULT_INFLUXDB_URL)
        token = os.environ.get('INFLUXDB_TOKEN')
        org = os.environ.get('INFLUXDB_ORG', DEFAULT_INFLUXDB_ORG)

        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        return cls(client, bucket=bucket)
