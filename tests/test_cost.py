from wise.cost import Cost
from wise.cost import get_cost


def test_get_cost():
    source = "GBP"
    amount = 1000
    target = "USD"

    cost = get_cost(source=source, amount=amount, target=target)

    assert isinstance(cost, Cost)
    assert cost.price.sourceCcy == source
    assert cost.price.targetAmount == amount
    assert cost.price.targetCcy == target
