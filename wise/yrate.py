import pandas as pd
import yfinance as yf
from pydantic import BaseModel
from retry import retry


class Ticker(BaseModel):
    Datetime: pd.Timestamp
    Open: float
    High: float
    Low: float
    Close: float
    Volume: float


@retry(delay=1)
def rates(from_curr, to_curr):
    if from_curr == to_curr:
        return 1.0

    symbol = f'{from_curr}{to_curr}=x'
    if to_curr == 'TWD' and from_curr != 'USD':
        return rates(from_curr, 'USD') * rates('USD', to_curr)

    df = yf.Ticker(symbol).history(period='1d', interval='1m')
    df = df.reset_index()
    t = Ticker.parse_obj(df.iloc[-1].to_dict())
    return float(t.Close)
