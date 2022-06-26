# vim: set fileencoding=utf-8:


from coronado import CardAccount
from coronado import CardAccountIdentifier
from coronado import CardProgram
from coronado import CoronadoMalformedObject
from coronado import OfferActivations
from coronado.testobjects import TEST_CARD_ACCOUNT_DICT
from coronado.testobjects import TEST_CARD_ACCOUNT_IDENTIFIER_DICT
from coronado.testobjects import TEST_CARD_ACCOUNT_IDENTIFIER_JSON
from coronado.testobjects import TEST_CARD_ACCOUNT_JSON
from coronado.testobjects import TEST_CARD_PROGRAM_DICT
from coronado.testobjects import TEST_CARD_PROGRAM_JSON
from coronado.testobjects import TEST_OFFER_ACTIVATIONS_DICT
from coronado.testobjects import TEST_OFFER_ACTIVATIONS_JSON

import pytest


# *** constants ***


# --- tests ---

def _createAndAssertObject(klass, pJSON, pDict, testKey = None, controlKey = None):
    with pytest.raises(CoronadoMalformedObject):
        klass(42)

    x = klass(pJSON)
    if testKey:
        assert x.__dict__[testKey] == pDict[controlKey]

    x = klass(pDict)
    if testKey:
        assert x.__dict__[testKey] == pDict[controlKey]


def test_APIObjectsInstantiation():
    _createAndAssertObject(CardAccount, TEST_CARD_ACCOUNT_JSON, TEST_CARD_ACCOUNT_DICT, 'objID', 'id')
    _createAndAssertObject(CardAccountIdentifier, TEST_CARD_ACCOUNT_IDENTIFIER_JSON, TEST_CARD_ACCOUNT_IDENTIFIER_DICT, 'cardProgramExternalID', 'card_program_external_id')
    _createAndAssertObject(CardProgram, TEST_CARD_PROGRAM_JSON, TEST_CARD_PROGRAM_DICT, 'publisherID', 'publisher_id')
    _createAndAssertObject(OfferActivations, TEST_OFFER_ACTIVATIONS_JSON, TEST_OFFER_ACTIVATIONS_DICT) 


# test_APIObjectsInstantiation()

