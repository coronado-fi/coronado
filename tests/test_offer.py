# vim: set fileencoding=utf-8:


from coronado.offer import MarketingFeeType
from coronado.offer import Offer
from coronado.offer import OfferCategory
from coronado.offer import OfferType


# import json
# import uuid

import coronado.auth as auth


# *** globals ***


# *** globals ***

_config = auth.loadConfig()
_auth = auth.Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'])

# TODO: The servicePath isn't initialized!
Offer.initialize(_config['serviceURL'], "", _auth)


# +++ tests +++

def test_MarketingFeeType():
    x = MarketingFeeType.PERCENTAGE

    assert isinstance(x, MarketingFeeType)
    assert str(x) == 'PERCENTAGE'
    assert str(x) == MarketingFeeType.PERCENTAGE.value



def test_OfferCatetory():
    x = OfferCategory.ENTERTAINMENT

    assert isinstance(x, OfferCategory)
    assert str(x) == 'ENTERTAINMENT'
    assert str(x) == OfferCategory.ENTERTAINMENT.value


def test_OfferType():
    x = OfferType.AFFILIATE

    assert x == OfferType.AFFILIATE
    assert str(x) == 'AFFILIATE'
    assert str(x) == OfferType.AFFILIATE.value


def test_Offer():
    x = Offer()

    assert isinstance(x, Offer)

