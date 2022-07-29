# vim: set fileencoding=utf-8:


from coronado import TripleEnum
from coronado import TripleObject
from coronado.baseobjects import BASE_OFFER_DICT


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


class OfferDeliveryMode(TripleEnum):
    """
    Offer delivery mode.
    """
    IN_PERSON = 'IN_PERSON'
    IN_PERSON_AND_ONLINE = 'IN_PERSON_AND_ONLINE'
    ONLINE = 'ONLINE'


class OfferType(TripleEnum):
    """
    Offer type definitions.
    """
    AFFILIATE = 'AFFILIATE'
    CARD_LINKED = 'CARD_LINKED'
    CATEGORICAL = 'CATEGORICAL'


class Offer(TripleObject):
    """
    The parent abstract class for all Coronado offer classes.
    """

    requiredAttributes = [
        # UNDER HEAVY CONSTRUCTION
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

