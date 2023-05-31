from wise.cost import Cost
from wise.payment import Payment


def main():
    source_currencies = [
        'AUD',
        'BGN',
        'BRL',
        'CAD',
        'CHF',
        'CZK',
        'DKK',
        'EUR',
        'GBP',
        'HUF',
        'IDR',
        'INR',
        'JPY',
        'NOK',
        'NZD',
        'PLN',
        'RON',
        'SEK',
        'SGD',
        'USD',
    ]
    for source_currency in source_currencies:
        payment = Payment().pay_with(source_currency).add(1000, 'USD')
        cost = Cost(payment)
        print(cost)


if __name__ == '__main__':
    main()
