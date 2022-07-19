# vim: set fileencoding=utf-8:


from coronado.rewards import Reward
from coronado.rewards import RewardStatus
from coronado.rewards import SERVICE_PATH

import pytest

import coronado.auth as auth


# *** constants ***


# *** globals ***

_config = auth.loadConfig()
_auth = auth.Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'])


Reward.initialize(_config['serviceURL'], SERVICE_PATH, _auth)


# *** tests ***

@pytest.mark.skip('There are no rewards for testing in dev or sandbox')
def test_Reward_list():
    rewards = Reward.list()
    rewards = Reward.list(status = RewardStatus.DISTRIBUTED_TO_CARDHOLDER)

# test_Reward_list()

