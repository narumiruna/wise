import wise


def main():
    print(wise.visa_rate())
    print(wise.wise_rate(target_amount=1000, source_currency='GBP', target_currency='USD'))


if __name__ == '__main__':
    main()
