from pydantic import BaseModel


class Price(BaseModel):
    priceSetId: int
    sourceAmount: float
    targetAmount: float
    payInMethod: str
    payOutMethod: str
    sourceCcy: str
    targetCcy: str
    total: float
    variableFee: float
    variableFeePercent: float
    swiftPayoutFlatFee: float
    flatFee: float
    midRate: float
    ecbRate: float
    ecbRateTimestamp: int
    ecbMarkupPercent: float
    additionalFeeDetails: dict
