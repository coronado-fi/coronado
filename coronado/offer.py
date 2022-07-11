# vim: set fileencoding=utf-8:


from coronado import CoronadoAPIError
from coronado import CoronadoDuplicatesDisallowedError
from coronado import CoronadoMalformedObjectError
from coronado import CoronadoUnexpectedError
from coronado import CoronadoUnprocessableObjectError
from coronado import TripleObject
from coronado.baseobjects import BASE_MERCHANT_CATEGORY_CODE_DICT
from coronado.baseobjects import BASE_OFFER_DICT

import enum
import json

import requests


# +++ constants +++

_SERVICE_PATH = 'partner/publishers'


# *** classes and objects ***


class MarketingFeeType(enum.Enum):
    """
    Offer fees may be expressed as percentages or fixed.
    """
    FIXED = 'FIXED'
    PERCENTAGE = 'PERCENTAGE'


    def __str__(self) -> str:
        return self.value


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
        'expirationDate',
        'externalID',
        'headline',
        'isActivated',
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



