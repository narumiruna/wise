from tqdm import tqdm

from wisest import query_currencies
from wisest import query_price


def main() -> None:
    codes = []
    for currency in tqdm(query_currencies()):
        try:
            query_price(source_currency=currency.code, target_amount=1000, target_currency="USD")
            codes.append(currency.code)
        except Exception as e:
            tqdm.write(f"unable to query price for {currency.code}, error: {e}")
    print(codes)


if __name__ == "__main__":
    main()
