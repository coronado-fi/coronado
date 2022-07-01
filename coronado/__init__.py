# vim: set fileencoding=utf-8:


from copy import deepcopy

from coronado.auth import Auth
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
from coronado.tools import tripleKeysToCamelCase

import json

import requests


# *** constants ***

__VERSION__ = '1.0.4'

API_URL = 'https://api.sandbox.tripleup.dev'



# +++ classes and objects +++

class CoronadoMalformedObjectError(Exception):
    """
    Raised when instantiating a Coronado object fails.  May also include
    a string describing the cause of the exception.
    """
    pass


class TripleObject(object):
    """
    Abstract class ancestor to all the triple API objects.
    """
    # +++ public +++

    def __init__(self, obj = None):
        if isinstance(obj, str):
            d = json.loads(obj)
        elif isinstance(obj, dict):
            d = deepcopy(obj)
        else:
            raise CoronadoMalformedObjectError

        d = tripleKeysToCamelCase(d)

        for key, value in d.items():
            if isinstance(value, (list, tuple)):
                setattr(self, key, [TripleObject(x) if isinstance(x, dict) else x for x in value])
            else:
                setattr(self, key, TripleObject(value) if isinstance(value, dict) else value)


    def assertAll(self, requiredAttributes: list) -> bool:
        """
        Asserts that all the attributes listed in the requiredAttributes list of
        attribute names are presein the final object.  Coronado/triple objects 
        are built from JSON inputs which may or may not include all required
        attributes.  This method ensures they do.

        Arguments:
            requiresAttributes - a list or tuple of string names
        
        Raises:
            CoronadoMalformedObjectError if one or more attributes are missing.
        """
        if requiredAttributes:
            attributes = self.__dict__.keys()
            if not all(attribute in attributes for attribute in requiredAttributes):
                missing = set(requiredAttributes)-set(attributes)
                raise CoronadoMalformedObjectError("attribute%s %s missing during instantiation" % ('' if len(missing) == 1 else 's', missing))


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

        requiredAttributes = [ 'completeAddress', ]

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


    @classmethod
    def list(klass : object, serviceURL = None, auth = None) -> list:
        """
        Return a list of all card accounts.

        Arguments
        ---------
        serviceURL : str
            The URL for the triple service API
        auth : coronado.auth.Auth
            An Auth object with a valid OAuth2 token

        Returns
        -------
        A list of CardAccount objects
        """
        endpoint = '/'.join([serviceURL, 'partner/card-accounts']) # URL fix later
        headers = { 'Authorization': ' '.join([ auth.tokenType, auth.token, ]) }
        response = requests.request('GET', endpoint, headers = headers)
        result = [ TripleObject(obj) for obj in json.loads(response.content)['card_accounts'] ]

        return result


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

