from wise.cost import Cost
from wise.payment import Payment
import json


def save_json(obj, f):
    with open(f, 'w') as f:
        json.dump(obj, f)


def main():
    source_currencies = ['GBP', 'EUR', 'CAD', 'JPY', 'AUD']
    text = ''
    for source_currency in source_currencies:
        payment = Payment().pay_with(source_currency).add(1000, 'USD')
        cost = Cost(payment)

        print(cost)
        text += str(cost) + '\n'

    payload = {"text": "Wise", "blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": text}}]}
    save_json(payload, 'payload.json')


if __name__ == '__main__':
    main()
