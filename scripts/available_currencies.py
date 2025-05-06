from wisest import query_currencies
from wisest import query_price


def main() -> None:
    codes = []
    for currency in query_currencies():
        try:
            query_price(source_currency=currency.code, target_amount=1000, target_currency="USD")
            codes.append(currency.code)
        except Exception as e:
            print(f"unable to query price for {currency.code}, error: {e}")
    print(codes)


if __name__ == "__main__":
    main()
