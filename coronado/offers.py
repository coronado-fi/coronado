# vim: set fileencoding=utf-8:


from coronado import CoronadoAPIError
from coronado import CoronadoDuplicatesDisallowedError
from coronado import CoronadoMalformedObjectError
from coronado import CoronadoUnexpectedError
from coronado import CoronadoUnprocessableObjectError
from coronado import TripleObject
from coronado.baseobjects import BASE_MERCHANT_CATEGORY_CODE_DICT
from coronado.baseobjects import BASE_OFFER_DICT

import json

import requests


# +++ constants +++

_SERVICE_PATH = 'partner/publishers'


# *** classes and objects ***


class MerchantCategoryCode(TripleObject):
    """
    A Merchant Category Code, or MCC, is a 4-digit number that indicates a line
    of business and the types of goods and services that the business provides
    to their customers.

    <a href='https://www.merchantmaverick.com/merchant-category-code-mcc/' target='_blank'>Merchant Category Codes (MCC):</a>
    All You Need to Know from *Maverick Merchant*.
    """
    requiredAttributes = [ 'code', 'description', ]


    def __init__(self, obj = BASE_MERCHANT_CATEGORY_CODE_DICT):
        """
        Create a new MCC instance.

        spec:

        ```
        {
            'code': '4269',
            'description': 'Aquaria, Dolphinaria, Seaquaria, and Zoos',
        }
        ```
        """
        TripleObject.__init__(self, obj)


    def __str__(self):
        return '%s: %s' % (self.code, self.description)


    def inSnakeCaseJSON(self) -> str:
        """
        Return a JSON representation of the receiver with the attributes
        written in snake_case format.

        Return
        ------
            A string with a JSON representation of the receiver.

        """
        return json.dumps(self.asSnakeCaseDictionary())


    def asSnakeCaseDictionary(self) -> dict:
        """
        Return a dict representation of the receiver with the attributes
        written in snake_case format.

        Return
        ------
            A dict representation of the receiver.
        """
        return { 'code': self.code, 'description': self.description, }


class Offer(TripleObject):
    """
    Offer objects represent offers from brands and retaliers linked to a payment
    provider like a debit or credit card.  The offer is redeemed by the consumer
    when the linked payment card is used at a point-of-sale.  Offer instances 
    connect on-line advertising campaings with concrete purchases.
    """

    requiredAttributes = [
        'objID',
        'activationRequired',
        'currencyCode',
        'effectiveDate',
        'isActivated',
        'headline',
        'minimumSpend',
        'mode',
        'rewardType',
        'type',
    ]


    def __init__(self, obj = BASE_OFFER_DICT):
        """
        Create a new Offer instance.

        spec:

        ```
        {
            'lorem': 'ipsum',
        }
        ```
        """
        TripleObject.__init__(self, obj)

# TODO: These objects must be implemented before Offer because some of the 
#       attributes are of these classes:
#
#       1. MerchantCategoryCode
#       2. Merchant

