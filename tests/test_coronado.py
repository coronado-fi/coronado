# vim: set fileencoding=utf-8:


from copy import deepcopy

from coronado import Address
from coronado import CardAccount
from coronado import CardAccountIdentifier
from coronado import CardAccountStatus
from coronado import CardProgram
from coronado import CoronadoMalformedObjectError
from coronado import MerchantCategoryCode
from coronado import MerchantLocation
from coronado import Offer
from coronado import OfferActivation
from coronado import OfferDisplayRules
from coronado import Publisher
from coronado import Reward
from coronado import Transaction
from coronado import TripleObject
from coronado.auth import Auth
from coronado.auth import Scopes
from coronado.baseobjects import BASE_ADDRESS_DICT
from coronado.baseobjects import BASE_ADDRESS_JSON
from coronado.baseobjects import BASE_CARD_ACCOUNT_DICT
from coronado.baseobjects import BASE_CARD_ACCOUNT_IDENTIFIER_DICT
from coronado.baseobjects import BASE_CARD_ACCOUNT_IDENTIFIER_JSON
from coronado.baseobjects import BASE_CARD_ACCOUNT_JSON
from coronado.baseobjects import BASE_CARD_PROGRAM_DICT
from coronado.baseobjects import BASE_CARD_PROGRAM_JSON
from coronado.baseobjects import BASE_MERCHANT_CATEGORY_CODE_DICT
from coronado.baseobjects import BASE_MERCHANT_CATEGORY_CODE_JSON
from coronado.baseobjects import BASE_MERCHANT_LOCATION_DICT
from coronado.baseobjects import BASE_MERCHANT_LOCATION_JSON
from coronado.baseobjects import BASE_OFFER_ACTIVATION_DICT
from coronado.baseobjects import BASE_OFFER_ACTIVATION_JSON
from coronado.baseobjects import BASE_OFFER_DICT
from coronado.baseobjects import BASE_OFFER_DISPLAY_RULES_DICT
from coronado.baseobjects import BASE_OFFER_DISPLAY_RULES_JSON
from coronado.baseobjects import BASE_OFFER_JSON
from coronado.baseobjects import BASE_PUBLISHER_DICT
from coronado.baseobjects import BASE_PUBLISHER_JSON
from coronado.baseobjects import BASE_REWARD_DICT
from coronado.baseobjects import BASE_REWARD_JSON
from coronado.baseobjects import BASE_TRANSACTION_DICT
from coronado.baseobjects import BASE_TRANSACTION_JSON

import pytest

import coronado.auth as auth


# *** constants ***


# *** globals ***

_config = auth.loadConfig()


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
    _createAndAssertObject(Address, BASE_ADDRESS_JSON, BASE_ADDRESS_DICT, 'completeAddress', 'complete_address')
    _createAndAssertObject(CardAccount, BASE_CARD_ACCOUNT_JSON, BASE_CARD_ACCOUNT_DICT, 'objID', 'id')
    _createAndAssertObject(CardAccountIdentifier, BASE_CARD_ACCOUNT_IDENTIFIER_JSON, BASE_CARD_ACCOUNT_IDENTIFIER_DICT, 'cardProgramExternalID', 'card_program_external_id')
    _createAndAssertObject(CardProgram, BASE_CARD_PROGRAM_JSON, BASE_CARD_PROGRAM_DICT, 'publisherID', 'publisher_id')
    _createAndAssertObject(MerchantCategoryCode, BASE_MERCHANT_CATEGORY_CODE_JSON, BASE_MERCHANT_CATEGORY_CODE_DICT, 'description', 'description')
    _createAndAssertObject(MerchantLocation, BASE_MERCHANT_LOCATION_JSON, BASE_MERCHANT_LOCATION_DICT, 'isOnline', 'is_online')
    _createAndAssertObject(Offer, BASE_OFFER_JSON, BASE_OFFER_DICT, 'activationRequired', 'activation_required')
    _createAndAssertObject(OfferActivation, BASE_OFFER_ACTIVATION_JSON, BASE_OFFER_ACTIVATION_DICT) 
    _createAndAssertObject(OfferDisplayRules, BASE_OFFER_DISPLAY_RULES_JSON, BASE_OFFER_DISPLAY_RULES_DICT, 'action', 'action')
    _createAndAssertObject(Publisher, BASE_PUBLISHER_JSON, BASE_PUBLISHER_DICT, 'assumedName', 'assumed_name')
    _createAndAssertObject(Reward, BASE_REWARD_JSON, BASE_REWARD_DICT, 'merchantName', 'merchant_name')
    _createAndAssertObject(Transaction, BASE_TRANSACTION_JSON, BASE_TRANSACTION_DICT, 'transactionType', 'transaction_type')


def test_CardAccount_list():
    auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scopes.PUBLISHERS)

    accounts = CardAccount.list(_config['serviceURL'], auth)

    assert isinstance(accounts, list)

    account = accounts[0]
    assert isinstance(account, TripleObject)
    assert account.objID


def test_CardAccount_create():
    auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scopes.PUBLISHERS)
    accountSpec = {
        'card_progream_external_id': 'RebatesNation24',
        'external_id': 'PNC-card-69',
        'status': CardAccountStatus.ENROLLED.value,
        'publisher_external_id': 'PNCBANK',
    }

    with pytest.raises(CoronadoMalformedObjectError):
        CardAccount.create(None, _config['serviceURL'], auth)
    
    account = CardAccount.create(accountSpec, _config['serviceURL'], auth)

    assert account
    


def test_CardAccount_byID():
    auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scopes.PUBLISHERS)
    accountID = 'bogusID'

    account = CardAccount.byID(_config['serviceURL'], accountID, auth)

    assert not account
    


test_CardAccount_create()
# test_CardAccount_byID()

