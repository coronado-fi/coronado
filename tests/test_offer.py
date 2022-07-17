# vim: set fileencoding=utf-8:


# from coronado import CoronadoDuplicatesDisallowedError
# from coronado import CoronadoMalformedObjectError
# from coronado import CoronadoUnprocessableObjectError
# from coronado import TripleObject
# from coronado.baseobjects import BASE_MERCHANT_CATEGORY_CODE_DICT
from coronado.offer import MarketingFeeType
from coronado.offer import Offer
from coronado.offer import OfferCategory
from coronado.offer import OfferType


# import json
# import uuid

# import pytest

# import coronado.auth as auth


# *** globals ***


# *** globals ***

# TODO: Pending Offer implementation
# _config = auth.loadConfig()
# _auth = auth.Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = auth.Scopes.PORTFOLIOS)
#
# Offer.initialize(_config['serviceURL'], SERVICE_PATH, _auth)


# +++ tests +++


def test_MarketingFeeType():
    x = MarketingFeeType.PERCENTAGE

    assert isinstance(x, MarketingFeeType)
    assert str(x) == "PERCENTAGE"
    assert str(x) == MarketingFeeType.PERCENTAGE.value


def test_OfferCatetory():
    x = OfferCategory.ENTERTAINMENT

    assert isinstance(x, OfferCategory)
    assert str(x) == "ENTERTAINMENT"
    assert str(x) == OfferCategory.ENTERTAINMENT.value


def test_OfferType():
    x = OfferType.AFFILIATE

    assert x == OfferType.AFFILIATE
    assert str(x) == "AFFILIATE"
    assert str(x) == OfferType.AFFILIATE.value


def test_Offer():
    x = Offer()

    assert isinstance(x, Offer)
