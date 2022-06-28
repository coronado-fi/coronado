# vim: set fileencoding=utf-8:


from copy import deepcopy

from coronado.tools import tripleKeysToCamelCase
from coronado.baseobjects import BASE_ADDRESS_DICT
from coronado.baseobjects import BASE_CARD_ACCOUNT_DICT
from coronado.baseobjects import BASE_CARD_ACCOUNT_IDENTIFIER_DICT
from coronado.baseobjects import BASE_CARD_PROGRAM_DICT
from coronado.baseobjects import BASE_MERCHANT_CATEGORY_CODE_DICT
from coronado.baseobjects import BASE_MERCHANT_LOCATION_DICT
from coronado.baseobjects import BASE_OFFER_ACTIVATION_DICT
from coronado.baseobjects import BASE_OFFER_DICT
from coronado.baseobjects import BASE_OFFER_DISPLAY_RULES_DICT
from coronado.baseobjects import BASE_PUBLISHER_DICT
from coronado.baseobjects import BASE_REWARD_DICT
from coronado.baseobjects import BASE_TRANSACTION_DICT

import json


# *** constants ***

__VERSION__ = '1.0.2'


# +++ classes and objects +++

class CoronadoMalformedObject(Exception):
    pass


class TripleObject(object):
    # +++ public +++

    def __init__(self, obj = None):
        if isinstance(obj, str):
            d = json.loads(obj)
        elif isinstance(obj, dict):
            d = deepcopy(obj)
        else:
            raise CoronadoMalformedObject

        d = tripleKeysToCamelCase(d)

        for key, value in d.items():
            if isinstance(value, (list, tuple)):
                setattr(self, key, [TripleObject(x) if isinstance(x, dict) else x for x in value])
            else:
                setattr(self, key, TripleObject(value) if isinstance(value, dict) else value)


    def assertAll(self, requiredAttributes: list) -> bool:
        attributes = self.__dict__.keys()
        if not all(attribute in attributes for attribute in requiredAttributes):
            raise CoronadoMalformedObject("missing attributes during instantiation")


    def listAttributes(self) -> dict:
        """
        Lists all the attributes and their type of the receiving object in the form:

        attrName : type
        
        Return:
            a dictionary of objects and types
        """
        keys = sorted(self.__dict__.keys())
        result = dict([ (key, str(type(self.__dict__[key])).replace('class ', '').replace("'", "").replace('<','').replace('>', '')) for key in keys ])

        return result


class Address(TripleObject):
    def __init__(self, obj = BASE_ADDRESS_DICT):
        TripleObject.__init__(self, obj)

        requiredAttributes = ['completeAddress', ]

        self.assertAll(requiredAttributes)


class CardAccountIdentifier(TripleObject):
    def __init__(self, obj = BASE_CARD_ACCOUNT_IDENTIFIER_DICT):
        TripleObject.__init__(self, obj)

        requiredAttributes = ['cardProgramExternalID', ]

        self.assertAll(requiredAttributes)


class CardAccount(TripleObject):
    def __init__(self, obj = BASE_CARD_ACCOUNT_DICT):
        TripleObject.__init__(self, obj)

        requiredAttributes = ['objID', 'cardProgramID', 'externalID', 'status', 'createdAt', 'updatedAt', ]

        self.assertAll(requiredAttributes)


class CardProgram(TripleObject):
    def __init__(self, obj = BASE_CARD_PROGRAM_DICT):
        TripleObject.__init__(self, obj)

        requiredAttributes = ['externalID', 'name', 'programCurrency', ]

        self.assertAll(requiredAttributes)


class MerchantCategoryCode(TripleObject):
    def __init__(self, obj = BASE_MERCHANT_CATEGORY_CODE_DICT):
        TripleObject.__init__(self, obj)

        requiredAttributes = [ 'code', 'description', ]

        self.assertAll(requiredAttributes)


class MerchantLocation(TripleObject):
    def __init__(self, obj = BASE_MERCHANT_LOCATION_DICT):
        TripleObject.__init__(self, obj)

        requiredAttributes = [ 'objID', 'isOnline', 'address', ]

        self.assertAll(requiredAttributes)


class Offer(TripleObject):
    def __init__(self, obj = BASE_OFFER_DICT):
        TripleObject.__init__(self, obj)

        requiredAttributes = [ 'objID', 'activationRequired', 'currencyCode', 'effectiveDate', 'isActivated', 'headline', 'minimumSpend', 'mode', 'rewardType', 'type', ]

        self.assertAll(requiredAttributes)


class OfferActivation(TripleObject):
    def __init__(self, obj = BASE_OFFER_ACTIVATION_DICT):
        TripleObject.__init__(self, obj)

        requiredAttributes = ['objID', 'cardAccountID', 'activatedAt', 'offer', ]

        self.assertAll(requiredAttributes)


class OfferDisplayRules(TripleObject):
    def __init__(self, obj = BASE_OFFER_DISPLAY_RULES_DICT):
        TripleObject.__init__(self, obj)

        requiredAttributes = ['action', 'scope', 'type', 'value', ]

        self.assertAll(requiredAttributes)


class Publisher(TripleObject):
    def __init__(self, obj = BASE_PUBLISHER_DICT):
        TripleObject.__init__(self, obj)

        requiredAttributes = [ 'objID', 'assumedName', 'address', 'createdAt', 'updatedAt', ]

        self.assertAll(requiredAttributes)


class Reward(TripleObject):
    def __init__(self, obj = BASE_REWARD_DICT):
        TripleObject.__init__(self, obj)

        requiredAttributes = [ 'transactionID', 'offerID', 'transactionDate', 'transactionAmount', 'transactionCurrencyCode', 'merchantName', 'status', ]

        self.assertAll(requiredAttributes)


class Transaction(TripleObject):
    def __init__(self, obj = BASE_TRANSACTION_DICT):
        TripleObject.__init__(self, obj)

        requiredAttributes = [ 'objID', 'cardAccountID', 'externalID', 'localDate', 'debit', 'amount', 'currencyCode', 'transactionType', 'description', 'matchingStatus', 'createdAt', 'updatedAt', ]

        self.assertAll(requiredAttributes)

