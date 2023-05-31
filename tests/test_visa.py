from wise.visa import get_visa_fx_rate
from wise.visa import FxRate


def test_get_visa_fx_rate():
    amount = 1.0
    from_curr = 'TWD'
    to_curr = 'USD'
    fee = 0.0

    fx_rate = get_visa_fx_rate(amount=amount, from_curr=from_curr, to_curr=to_curr, fee=fee)
    assert isinstance(fx_rate, FxRate)
    assert fx_rate.conversionAmountValue == str(amount)
    assert fx_rate.conversionFromCurrency == from_curr
    assert fx_rate.conversionToCurrency == to_curr
