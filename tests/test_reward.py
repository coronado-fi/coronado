# vim: set fileencoding=utf-8:


from coronado import CoronadoForbiddenError
from coronado import TripleObject
from coronado.reward import Reward
from coronado.reward import RewardStatus
from coronado.reward import SERVICE_PATH

import pytest

import coronado.auth as auth


# *** constants ***


# *** globals ***

_config = auth.loadConfig()
_auth = auth.Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = auth.Scope.CONTENT_PROVIDERS)

Reward.initialize(_config['serviceURL'], SERVICE_PATH, _auth)


# *** tests ***

@pytest.mark.skip('Not implemented yet')
def test_RewardType():
    None


# @pytest.mark.skip('The service throws 500-series errors on some calls')
def test_Reward_list():
    rewards = Reward.list()
    assert isinstance(rewards, list)
    if len(rewards):
        reward = rewards[0]
        assert isinstance(reward, TripleObject)
        assert reward.transactionID

    rewards = Reward.list(status = RewardStatus.DENIED_BY_MERCHANT)
    assert isinstance(rewards, list)
    if len(rewards):
        reward = rewards[0]
        assert isinstance(reward, TripleObject)
        assert reward.transactionID

    rewards = Reward.list(status = RewardStatus.DISTRIBUTED_TO_CARDHOLDER)
    assert isinstance(rewards, list)
    if len(rewards):
        reward = rewards[0]
        assert isinstance(reward, TripleObject)
        assert reward.transactionID

    rewards = Reward.list(status = RewardStatus.DISTRIBUTED_TO_PUBLISHER)
    assert isinstance(rewards, list)
    if len(rewards):
        reward = rewards[0]
        assert isinstance(reward, TripleObject)
        assert reward.transactionID

    rewards = Reward.list(status = RewardStatus.PENDING_MERCHANT_APPROVAL)
    assert isinstance(rewards, list)
    if len(rewards):
        reward = rewards[0]
        assert isinstance(reward, TripleObject)
        assert reward.transactionID

    rewards = Reward.list(status = RewardStatus.PENDING_MERCHANT_FUNDING)
    assert isinstance(rewards, list)
    if len(rewards):
        reward = rewards[0]
        assert isinstance(reward, TripleObject)
        assert reward.transactionID

    rewards = Reward.list(status = RewardStatus.PENDING_TRANSFER_TO_PUBLISHER)
    assert isinstance(rewards, list)
    if len(rewards):
        reward = rewards[0]
        assert isinstance(reward, TripleObject)
        assert reward.transactionID

    rewards = Reward.list(status = RewardStatus.REJECTED)
    assert isinstance(rewards, list)
    if len(rewards):
        reward = rewards[0]
        assert isinstance(reward, TripleObject)
        assert reward.transactionID


def test_Reward_approve():
    approvedCount = len(Reward.list(status = RewardStatus.PENDING_MERCHANT_FUNDING))
    reward = Reward.list(status = RewardStatus.PENDING_MERCHANT_APPROVAL)[0]
    result = Reward.approve(reward.transactionID, reward.offerID)
    assert result
    assert len(Reward.list(status = RewardStatus.PENDING_MERCHANT_FUNDING)) == approvedCount+1

    result = Reward.approve(reward.transactionID, reward.offerID) # already approved
    assert not result

 
def test_Reward_outOfScope():
    localAuth = auth.Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = auth.Scope.VIEW_OFFERS)
    Reward.initialize(_config['serviceURL'], SERVICE_PATH, localAuth)

    with pytest.raises(CoronadoForbiddenError):
        Reward.list()

    Reward.initialize(_config['serviceURL'], SERVICE_PATH, _auth)
    Reward.list()

