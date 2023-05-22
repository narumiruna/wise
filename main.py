from wise.cost import Cost
from wise.payment import Payment


def main():
    source_currencies = ['GBP', 'EUR', 'CAD', 'JPY', 'AUD']
    for source_currency in source_currencies:
        payment = Payment().pay_with(source_currency).add(1000, 'USD')
        cost = Cost(payment)
        print(cost)


if __name__ == '__main__':
    main()
