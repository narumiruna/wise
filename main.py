from loguru import logger

import wise
from wise.utils import get_bank_transfer_in_balance_out
from wise.cost import Cost
from wise.payment import Payment

SOURCE_CURRENCIES = ['GBP', 'EUR', 'CAD']


def calculate_wise_fee(source_currency: float, target_amount: float, target_currency: str, card_fee: float):
    source_twd_rate = float(wise.get_visa_fx_rate(from_curr='TWD', to_curr=source_currency).fxRateWithAdditionalFee)

    # 取得 wise 的價格
    prices = wise.get_wise_prices(target_amount=target_amount,
                                  source_currency=source_currency,
                                  target_currency=target_currency)
    # 找出銀行轉帳到 wise balance 的價格
    # 使用 Google Pay 的 PayInMethod 會是 Bank Transfer
    price = get_bank_transfer_in_balance_out(prices)

    # source amount 是用信用卡的付款金額
    source_amount = price.sourceAmount
    # 轉換成新台幣
    payment_in_twd = source_amount * source_twd_rate
    logger.info('Payment: {} {} = {} TWD', source_amount, source_currency, payment_in_twd)

    # 計算信用卡國外刷卡的手續費
    # 預設是 1.5%
    card_fee_in_twd = payment_in_twd * card_fee
    logger.info('Card Fee: {} TWD', card_fee_in_twd)

    # 計算可以獲得的哩程
    miles = payment_in_twd / 10.0
    logger.info('Miles: {}', miles)

    # 取得目標貨幣對台幣的匯率
    target_currency_in_twd = float(
        wise.get_visa_fx_rate(from_curr='TWD', to_curr=target_currency).fxRateWithAdditionalFee)
    logger.info('{}TWD: {}', target_currency, target_currency_in_twd)

    # 計算 wise 的手續費
    wise_fee_in_twd = payment_in_twd - target_amount * target_currency_in_twd
    logger.info('Wise Fee: {} TWD', wise_fee_in_twd)

    # 計算最後信用卡要付的總金額
    total_payment_in_twd = payment_in_twd + card_fee_in_twd
    logger.info('Total Payment: {} TWD', total_payment_in_twd)

    # 計算 wise 的手續費 加上 信用卡手續費的總金額
    # 以及所有手續費的百分比
    total_fee_in_twd = wise_fee_in_twd + card_fee_in_twd
    fee_in_percent = 100 * total_fee_in_twd / total_payment_in_twd
    logger.info('Total Fee: {}({:.2f}%) TWD', total_fee_in_twd, fee_in_percent)


def main():
    for source_currency in SOURCE_CURRENCIES:
        payment = Payment().pay_with(source_currency).add(1000, 'USD')
        cost = Cost(payment)
        print(cost)


if __name__ == '__main__':
    main()
