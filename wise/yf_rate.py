import yfinance as yf
from retry import retry


@retry(delay=1)
def get_fx_rate(from_curr, to_curr):
    if from_curr == to_curr:
        return 1.0

    symbol = f"{from_curr}{to_curr}=x"
    if to_curr == "TWD" and from_curr != "USD":
        return get_fx_rate(from_curr, "USD") * get_fx_rate("USD", to_curr)

    df = yf.Ticker(symbol).history(period="1d", interval="1m")
    df = df.reset_index()
    return float(df.iloc[-1]["Close"])
