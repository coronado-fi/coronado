# vim: set fileencoding=utf-8:


from coronado.reward import RewardType


# *** constants ***


# *** tests ***

def test_RewardType():
    x = RewardType.AFFILIATE

    assert x == RewardType.AFFILIATE
    assert str(x) == 'AFFILIATE'
    assert str(x) == RewardType.AFFILIATE.value

