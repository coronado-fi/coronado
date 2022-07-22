# vim: set fileencoding=utf-8:


from copy import deepcopy

# from coronado import CardAccountIdentifier
# from coronado import MerchantCategoryCode
# from coronado import MerchantLocation
# from coronado import Offer
# from coronado import OfferActivation
# from coronado import OfferDisplayRules
# from coronado import Reward
# from coronado import Transaction
# from coronado.baseobjects import BASE_CARD_ACCOUNT_IDENTIFIER_DICT
# from coronado.baseobjects import BASE_CARD_ACCOUNT_IDENTIFIER_JSON
# from coronado.baseobjects import BASE_MERCHANT_CATEGORY_CODE_DICT
# from coronado.baseobjects import BASE_MERCHANT_CATEGORY_CODE_JSON
# from coronado.baseobjects import BASE_MERCHANT_LOCATION_DICT
# from coronado.baseobjects import BASE_MERCHANT_LOCATION_JSON
# from coronado.baseobjects import BASE_OFFER_ACTIVATION_DICT
# from coronado.baseobjects import BASE_OFFER_ACTIVATION_JSON
# from coronado.baseobjects import BASE_OFFER_DICT
# from coronado.baseobjects import BASE_OFFER_DISPLAY_RULES_DICT
# from coronado.baseobjects import BASE_OFFER_DISPLAY_RULES_JSON
# from coronado.baseobjects import BASE_OFFER_JSON
# from coronado.baseobjects import BASE_REWARD_DICT
# from coronado.baseobjects import BASE_REWARD_JSON
# from coronado.baseobjects import BASE_TRANSACTION_DICT
# from coronado.baseobjects import BASE_TRANSACTION_JSON
from coronado import CoronadoMalformedObjectError
from coronado import TripleEnum
from coronado import TripleObject
from coronado.address import Address
from coronado.auth import Auth
from coronado.auth import Scope
from coronado.baseobjects import BASE_ADDRESS_DICT
from coronado.baseobjects import BASE_ADDRESS_JSON
from coronado.baseobjects import BASE_CARD_ACCOUNT_DICT
from coronado.baseobjects import BASE_CARD_ACCOUNT_JSON
from coronado.baseobjects import BASE_CARD_PROGRAM_DICT
from coronado.baseobjects import BASE_CARD_PROGRAM_JSON
from coronado.baseobjects import BASE_MERCHANT_DICT
from coronado.baseobjects import BASE_MERCHANT_JSON
from coronado.baseobjects import BASE_PUBLISHER_DICT
from coronado.baseobjects import BASE_PUBLISHER_JSON
from coronado.cardaccount import CardAccount
from coronado.cardprog import CardProgram
from coronado.merchant import Merchant
from coronado.publisher import Publisher

import pytest

import coronado.auth as auth


# *** constants ***


# *** globals ***

_config = auth.loadConfig()
_auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scope.PUBLISHERS)


# --- tests ---

def _createAndAssertObject(klass, pJSON, pDict, testKey = None, controlKey = None):
    with pytest.raises(CoronadoMalformedObjectError):
        klass(42)

    x = klass(pJSON)
    if testKey:
        assert x.__dict__[testKey] == pDict[controlKey]

    x = klass(pDict)
    if testKey:
        assert x.__dict__[testKey] == pDict[controlKey]


def test_TripleObject():
    x = TripleObject(BASE_PUBLISHER_DICT)
    y = x.listAttributes()

    assert 'portfolioManagerID' in y.keys()

    z = Publisher(x)
    assert isinstance(z, Publisher)


def test_TripleObjectMissingAttrError():
    x = deepcopy(BASE_PUBLISHER_DICT)
    del(x['assumed_name'])

    try:
        Publisher(x)
    except CoronadoMalformedObjectError as e:
        assert str(e) == "attribute {'assumedName'} missing during instantiation"

    del(x['address'])
    with pytest.raises(CoronadoMalformedObjectError) as e:
        Publisher(x)
        assert str(e) == "attributes {'assumedName', 'address'} missing during instantiation"


def test_APIObjectsInstantiation():
    _createAndAssertObject(Address, BASE_ADDRESS_JSON, BASE_ADDRESS_DICT, 'countryCode', 'country_code')
    _createAndAssertObject(CardAccount, BASE_CARD_ACCOUNT_JSON, BASE_CARD_ACCOUNT_DICT, 'objID', 'id')
    _createAndAssertObject(CardProgram, BASE_CARD_PROGRAM_JSON, BASE_CARD_PROGRAM_DICT, 'publisherID', 'publisher_id')
    _createAndAssertObject(Merchant, BASE_MERCHANT_JSON, BASE_MERCHANT_DICT, 'externalID', 'external_id')
    _createAndAssertObject(Publisher, BASE_PUBLISHER_JSON, BASE_PUBLISHER_DICT, 'assumedName', 'assumed_name')
#     _createAndAssertObject(CardAccountIdentifier, BASE_CARD_ACCOUNT_IDENTIFIER_JSON, BASE_CARD_ACCOUNT_IDENTIFIER_DICT, 'cardProgramExternalID', 'card_program_external_id')
#     _createAndAssertObject(MerchantCategoryCode, BASE_MERCHANT_CATEGORY_CODE_JSON, BASE_MERCHANT_CATEGORY_CODE_DICT, 'description', 'description')
#     _createAndAssertObject(MerchantLocation, BASE_MERCHANT_LOCATION_JSON, BASE_MERCHANT_LOCATION_DICT, 'isOnline', 'is_online')
#     _createAndAssertObject(Offer, BASE_OFFER_JSON, BASE_OFFER_DICT, 'activationRequired', 'activation_required')
#     _createAndAssertObject(OfferActivation, BASE_OFFER_ACTIVATION_JSON, BASE_OFFER_ACTIVATION_DICT)
#     _createAndAssertObject(OfferDisplayRules, BASE_OFFER_DISPLAY_RULES_JSON, BASE_OFFER_DISPLAY_RULES_DICT, 'action', 'action')
#     _createAndAssertObject(Reward, BASE_REWARD_JSON, BASE_REWARD_DICT, 'merchantName', 'merchant_name')
#     _createAndAssertObject(Transaction, BASE_TRANSACTION_JSON, BASE_TRANSACTION_DICT, 'transactionType', 'transaction_type')


def test_TripleObject_classVariables():
    # Uninitialized
    assert Address._serviceURL == CardAccount._serviceURL
    assert Address._auth == CardAccount._auth

    # Initialize one of them
    Address._serviceURL = 'https://example.com'
    Address._auth = { 'bogus': '42', }

    assert Address._serviceURL != CardAccount._serviceURL
    assert Address._auth != CardAccount._auth


def test_TripleObject_initialize():
    control = 'BOGUS'
    TripleObject.initialize(_config['serviceURL'], control, _auth)

    assert TripleObject._serviceURL == _config['serviceURL']
    assert TripleObject._servicePath == control
    assert 'python-coronado' in TripleObject.headers['User-Agent']

    badPath = '/%s' % control 
    TripleObject.initialize(_config['serviceURL'], badPath, _auth)
    assert TripleObject._servicePath == control

    badPath = '%s/' % control 
    TripleObject.initialize(_config['serviceURL'], badPath, _auth)
    assert TripleObject._servicePath == control

    badPath = '/%s/' % control 
    TripleObject.initialize(_config['serviceURL'], badPath, _auth)
    assert TripleObject._servicePath == control


def test_TripleObject_headers():
    # Must follow test_TripleObject_initialize() to work; it uses
    # the class variables.

    h = TripleObject.headers

    assert isinstance(h, dict)
    assert 'Authorization' in h
    assert 'User-Agent' in h


def test_TripleObject_requiredAttributes():
    class Synthetic(TripleObject):
        requiredAttributes = [ 'alpha', 'beta', ]

    s = Synthetic({ 'alpha': 42, 'theta_meta': 69, 'beta': 99, })
    assert 'thetaMeta' in s.listAttributes()

    with pytest.raises(CoronadoMalformedObjectError):
        Synthetic({ 'alpha': 42, 'theta_meta': 69, })


def test_TripleObject___str__():
    class Synthetic(TripleObject):
        requiredAttributes = [ 'alpha', 'beta', ]

    s = Synthetic({ 'alpha': 42, 'theta_meta': 69, 'beta': 99, })
    assert str(s)

    
def test_TripleEnum():
    class Bogus(TripleEnum):
        XX = 42
        YY = 69

    x = Bogus.XX

    assert x == Bogus.XX
    assert x.value == 42
    assert str(x) == '42'

