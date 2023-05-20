from loguru import logger

import wise
from wise.utils import get_bank_transfer_in_balance_out

SOURCE_CURRENCIES = ['GBP', 'EUR']


def main():
    target_amount = 1000
    card_fee = 0.015
    target_currency = 'USD'

    for source_currency in SOURCE_CURRENCIES:
        source_currency_in_twd = float(
            wise.visa_rate(amount=1, from_curr='TWD', to_curr=source_currency).fxRateWithAdditionalFee)

        prices = wise.wise_rate(target_amount=target_amount,
                                source_currency=source_currency,
                                target_currency=target_currency)
        price = get_bank_transfer_in_balance_out(prices)

        source_amount = price.sourceAmount
        logger.info('source amount: {} {}', source_amount, source_currency)

        payment_in_twd = source_amount * source_currency_in_twd
        logger.info('payment in TWD: {}', payment_in_twd)

        card_fee_in_twd = payment_in_twd * card_fee
        logger.info('card fee in TWD: {}', card_fee_in_twd)

        miles = payment_in_twd / 10.0
        logger.info('miles: {}', miles)

        target_currency_in_twd = float(
            wise.visa_rate(amount=1, from_curr='TWD', to_curr=target_currency).fxRateWithAdditionalFee)
        logger.info('{}TWD: {}', target_currency, target_currency_in_twd)

        wise_fee_in_twd = payment_in_twd - target_amount * target_currency_in_twd
        logger.info('wise fee in TWD: {}', wise_fee_in_twd)

        # 		totalFeeInTWD := wiseFeeInTWD + cardFeeInTWD
        total_fee_in_twd = wise_fee_in_twd + card_fee_in_twd
        logger.info('total fee in TWD: {}', total_fee_in_twd)

        total_payment_in_twd = payment_in_twd + card_fee_in_twd
        logger.info('total payment in TWD: {}', total_payment_in_twd)

        fee_in_percent = 100 * total_fee_in_twd / total_payment_in_twd
        logger.info('fee in percent: {}%', fee_in_percent)


if __name__ == '__main__':
    main()
