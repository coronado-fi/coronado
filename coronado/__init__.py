# vim: set fileencoding=utf-8:


from copy import deepcopy

from coronado.baseobjects import BASE_CARD_ACCOUNT_IDENTIFIER_DICT
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


# *** constants ***

__VERSION__ = '1.0.6'

API_URL = 'https://api.sandbox.tripleup.dev'
CORONADO_USER_AGENT = 'python-coronado/%s' % __VERSION__



# +++ classes and objects +++

class CoronadoAPIError(Exception):
    """
    Raised when the API server fails for some reason (HTTP status 5xx)
    and it's unrecoverable.  This error most often means that the
    service itself is misconfigured, is down, or has a serious bug.
    Printing the reason code will display as much information about why
    the service failed as it is available from the API system.
    """

class CoronadoDuplicatesDisallowed(Exception):
    """
    Raised when trying to create a Coronado/triple object based on an
    object spec that already exists (e.g. the externalID for the object
    is already registered with the service, or its assumed name is
    duplicated).
    """



class CoronadoMalformedObjectError(Exception):
    """
    Raised when instantiating a Coronado object fails.  May also include
    a string describing the cause of the exception.
    """
    pass


class CoronadoUnexpectedError(Exception):
    """
    Raised when performning a Coronado API call that results in an
    unknown, unexpected, undocumented, weird AF error that nobody knows
    how it happened.
    """


class CoronadoUnprocessableObjectError(Exception):
    """
    Raised when instantiating a Coronado object fails because the object
    is well-formed but contains semantic or object representation errors.
    """
    pass


class TripleObject(object):
    """
    Abstract class ancestor to all the triple API objects.
    """
    # +++ class variables ++

    auth = None
    serviceURL = None


    # +++ implementation +++

    # +++ public +++

    def __init__(self, obj = None):
        if isinstance(obj, str):
            d = json.loads(obj)
        elif isinstance(obj, dict):
            d = deepcopy(obj)
        elif isinstance(obj, TripleObject):
            d = deepcopy(obj.__dict__)
        else:
            raise CoronadoMalformedObjectError

        d = tripleKeysToCamelCase(d)

        for key, value in d.items():
            if isinstance(value, (list, tuple)):
                setattr(self, key, [TripleObject(x) if isinstance(x, dict) else x for x in value])
            else:
                setattr(self, key, TripleObject(value) if isinstance(value, dict) else value)


    @classmethod
    def initialize(klass, serviceURL : str, auth : object):
        """
        Initialize the class to use an appropriate service URL or authentication
        object.

        Arguments
        ---------
        serviceURL
            A string with an https locator pointing at the service top level URL
        auth
            An instance of Auth configured to use the the serviceURL within the
            defined scope
        """
        klass.serviceURL = serviceURL
        klass.auth = auth


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
    

    @classmethod
    @property
    def headers(klass):
        return {
            'Authorization': ' '.join([ klass.auth.tokenType, klass.auth.token, ]),
            'User-Agent': CORONADO_USER_AGENT,
        }


class CardAccountIdentifier(TripleObject):
    def __init__(self, obj = BASE_CARD_ACCOUNT_IDENTIFIER_DICT):
        TripleObject.__init__(self, obj)

        requiredAttributes = ['cardProgramExternalID', ]

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

