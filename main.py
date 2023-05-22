from wise.cost import Cost
from wise.payment import Payment

SOURCE_CURRENCIES = ['GBP', 'EUR', 'CAD']


def main():
    for source_currency in SOURCE_CURRENCIES:
        payment = Payment().pay_with(source_currency).add(1000, 'USD')
        cost = Cost(payment)
        print(cost)


if __name__ == '__main__':
    main()
