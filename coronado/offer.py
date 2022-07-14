# vim: set fileencoding=utf-8:


# from coronado import CoronadoAPIError
# from coronado import CoronadoDuplicatesDisallowedError
# from coronado import CoronadoMalformedObjectError
# from coronado import CoronadoUnexpectedError
# from coronado import CoronadoUnprocessableObjectError
# from coronado.baseobjects import BASE_MERCHANT_CATEGORY_CODE_DICT
from coronado import TripleEnum
from coronado import TripleObject
from coronado.baseobjects import BASE_OFFER_DICT
# 
# import json
# 
# import requests


# +++ constants +++

_SERVICE_PATH = 'partner/publishers'


# *** classes and objects ***


class MarketingFeeType(TripleEnum):
    """
    Offer fees may be expressed as percentages or fixed.
    """
    FIXED = 'FIXED'
    PERCENTAGE = 'PERCENTAGE'


class OfferCategory(TripleEnum):
    """
    High-level offer categories.  May be database-based in future
    implementations.
    """
    AUTOMOTIVE = 'AUTOMOTIVE'
    CHILDREN_AND_FAMILY = 'CHILDREN_AND_FAMILY'
    ELECTRONICS = 'ELECTRONICS'
    ENTERTAINMENT = 'ENTERTAINMENT'
    FINANCIAL_SERVICES = 'FINANCIAL_SERVICES'
    FOOD = 'FOOD'
    HEALTH_AND_BEAUTY = 'HEALTH_AND_BEAUTY'
    HOME = 'HOME'
    OFFICE_AND_BUSINESS = 'OFFICE_AND_BUSINESS'
    RETAIL = 'RETAIL'
    TRAVEL = 'TRAVEL'
    UTILITIES_AND_TELECOM = 'UTILITIES_AND_TELECOM'


class OfferDeliveryModes(TripleEnum):
    """
    Offer delivery mode.
    """
    IN_PERSON = 'IN_PERSON'
    IN_PERSON_AND_ONLINE = 'IN_PERSON_AND_ONLINE'
    ONLINE = 'ONLINE'


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

