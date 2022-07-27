# vim: set fileencoding=utf-8:


from coronado import TripleObject
from coronado.address import Address
from coronado.baseobjects import BASE_CLOFFER_DETAILS_DICT
from coronado.baseobjects import BASE_OFFER_SEARCH_RESULT_DICT
from coronado.exceptions import CallError
from coronado.exceptions import errorFor
from coronado.merchant import MerchantCategoryCode as MCC
from coronado.offer import Offer
from coronado.offer import OfferCategory
from coronado.offer import OfferDeliveryMode
from coronado.offer import OfferType

import json

import requests


# +++ constants +++

FETCH_RPC_SERVICE_PATH = 'partners/offer-display/details'
SEARCH_RPC_SERVICE_PATH = 'partner/offer-display/search-offers'


# *** classes and objects ***

class OfferSearchResult(Offer):
    """
    Offer search result.  Search results objects are only produced
    when executing a call to the `forQuery()` method.  Each result represents 
    an offer recommendation based on the caller's geolocation, transaction
    history, and offer interactions.

    OfferSearchResult objects can't be instantiated by themselves, and are
    always the result from running a query against the triple API.
    """

    # +++ private +++

    @classmethod
    def _queryWith(klass, spec):
        endpoint = '/'.join([ klass._serviceURL, klass._servicePath, ])
        response = requests.request('POST', endpoint, headers = klass.headers, json = spec)

        if response.status_code == 200:
            result = [ klass(offer) for offer in json.loads(response.content)['offers'] ]
        elif response.status_code == 404:
            result = None
        else:
            raise errorFor(response.status_code, response.text)

        return result


    @classmethod
    def _error(klass, someErrorClass, explanation):
        raise someErrorClass(explanation)


    # *** public ***

    requiredAttributes = [
        'objID',
        'activationRequired',
        'currencyCode',
        'effectiveDate',
        'externalID',
        'headline',
        'isActivated',
# TODO:  Bug! -- 20220718
#         'mode',
#         'rewardType',
        'score',
        'type',
    ]

    
    def __init__(self, obj = BASE_OFFER_SEARCH_RESULT_DICT):
        """
        Create a new OfferSearchResult instance.  Objects of this class should
        not be instantiated via constructor in most cases.  Use the `forQuery()`
        method to query the system for valid results.
        """
        TripleObject.__init__(self, obj)


    @classmethod
    def queryWith(klass, **args):
        """
        Search for offers that meet the query search criteria.  The underlying
        service allows for parameterized search and plain text searches.  The
        **<a href='https://api.tripleup.dev/docs' target='_blank'>Search Offers</a>**
        endpoint offers a full description of the object search capabilities.

        Arguments
        ---------
            cardAccountID
        A valid, known card account ID registered with the system

            countryCode
        The 2-letter ISO code for the country (e.g. US, MX, CA)

            filterCategory
        An offer category type filter; see coronado.offer.OfferType for details;
        valid values:  AUTOMOTIVE, CHILDREN_AND_FAMILY, ELECTRONICS,
        ENTERTAINMENT, FINANCIAL_SERVICES, FOOD, HEALTH_AND_BEAUTY, HOME,
        OFFICE_AND_BUSINESS, RETAIL, TRAVEL, UTILITIES_AND_TELECOM

            filterDeliveryMode
        An offer mode; see coronado.offer.OfferDeliveryMode for details; valid
        values:  IN_PERSON, IN_PERSON_AND_ONLINE, ONLINE,

            filterType
        An offer type filter; see coronado.offer.OfferType for details; valid
        values: AFFILIATE, CARD_LINKED, CATEGORICAL

            latitude
        The Earth latitude in degrees, with a whole and decimal part, e.g.
        40.46; relative to the equator

            longitude
        The Earth longitude in degrees, with a whole and decimal part, e.g.
        -79.92; relative to Greenwich

            pageSize
        The number of search results to return

            pageOffset
        The offset from the first result (inclusive) where to start fetching 
        results for this query

            postalCode
        The postalCode associated with the cardAccountID

            radius
        The radius, in meters, to find offers with merchants established
        within that distance to the centroid of the postal code

            spec
        A snake_case dictionary with the query request body.

            textQuery
        A text query to assist the back-end in further refinement of the query;
        free form text is allowed

        Sample spec (incomplete, for illustrative purposes only; see
        documentation for full spec):

        **Important**

        If `spec` is present, it overrides all other arguments used within its
        scope.  This implementation will ignore all other arguments and try to
        fetch the card linked offer details against the `spec` payload.

        Sample spec (incomplete, for illustrative purposes only; see
        documentation for full spec):

        ```
        {
          'proximity_target': {
            'postal_code': '15206',
            'country_code': 'US',
            'radius': 35000
          },
          'card_account_identifier': {
            'card_account_id': 'triple-abc-123'
          },
          'text_query': 'italian food',
          'page_size': 25,
          'page_offset': 0,
          'apply_filter': {
            'type': 'CARD_LINKED'
          }
        }

        ```

        Returns
        -------
            list of OfferSearchResult
        A list of offer search results.  The list may be empty/zero-length,
        or `None`.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the 
        **`coronado.exceptions`** module.
        """
        if 'spec' in args:
            # Uses spec, backward compatibility; new implementation is for
            # people who don't want to initialize the spec payload (FI
            # requirement).
            return klass._queryWith(args['spec'])

        requiredArgs = [
            'cardAccountID',
            'pageSize',
            'pageOffset',
        ]

        if not all(arg in args.keys() for arg in requiredArgs):
            missing = set(requiredArgs)-set(args.keys())
            raise CallError('argument%s %s missing during instantiation' % ('' if len(missing) == 1 else 's', missing))

        filters = dict()
        if 'filterCategory' in args:
            isinstance(args['filterCategory'], OfferCategory) \
                or klass._error(CallError, 'filterCategory must be an instance of %s' % OfferCategory)
            filters['category'] = str(args['filterCategory'])
        if 'filterMode' in args:
            isinstance(args['filterMode'], OfferDeliveryMode) \
                or klass._error(CallError, 'filterMode must be an instance of %s' % OfferDeliveryMode)
            filters['mode'] = str(args['filterMode'])
        if 'filterType' in args:
            isinstance(args['filterType'], OfferType) \
                or klass._error(CallError, 'filterType must be an instance of %s' % OfferType)
            filters['type'] = str(args['filterType'])

        try:
            spec = {
                # TODO:  what's the behavior if both coordinates and postal code + # 20220718 -- lat,long used; the rest is ignored
                #        country code are specified?
                'proximity_target': {
                    'latitude': args['latitude'],
                    'longitude': args['longitude'],
                    'radius': args['radius'],
                },
                'card_account_identifier': {
                    'card_account_id': args['cardAccountID'],
                },
                'text_query': args.get('textQuery', '').lower(),
                'page_size': args['pageSize'],
                'page_offset': args['pageOffset'],
                'apply_filter': filters,
            }
        except KeyError as e:
            raise CallError(str(e))

        return klass._queryWith(spec)


    @classmethod
    def create(klass, spec: dict) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def byID(klass, objID: str) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def updateWith(klass, objID: str, spec: dict) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def list(klass, paraMap = None, **args) -> list:
        """
        **Disabled for this class.**
        """
        None


def _assembleDetailsFrom(payload):
    # payload ::= JSON
    d = json.loads(payload)

    if 'offer' not in d:
        raise CallError('offer attribute not found')

    offer = CardLinkedOffer(d['offer'])
    offer.merchantCategoryCode = MCC(offer.merchantCategoryCode)
    # TODO: the category attribute is missing from the result - 20220718
    # offer.category = OfferCategory(offer.category)
    # TODO: the rewardType attribute is missing from the result - 20220718
    # offer.rewardType = OfferCategory(offer.rewardType)
    offer.tripleCategoryName = OfferCategory(offer.tripleCategoryName)
    offer.offerMode = OfferDeliveryMode(offer.offerMode)
    offer.type = OfferType(offer.type)

    merchantLocations = [ MerchantLocation(l) for l in d['merchant_locations'] ]

    for location in merchantLocations:
        location.address = Address(location.address)

    d['offer'] = offer
    d['merchant_locations'] = merchantLocations

    offerDetails = CardLinkedOfferDetails(d)

    return offerDetails


class CardLinkedOfferDetails(TripleObject):
    """
    Object representation of the offer details and associated merchant
    locations for an offer.
    """

    # --- private ---

    @classmethod
    def _forIDwithSpec(klass, objID: str, spec: dict, includeLocations: bool) -> object:
        endpoint = '/'.join([ klass._serviceURL, 'partner/offer-display/details', objID, ])
        response = requests.request('POST', endpoint, headers = klass.headers, json = spec)

        if response.status_code == 200:
            result = _assembleDetailsFrom(response.content)
        elif response.status_code == 404:
            result = None
        else:
            raise errorFor(response.status_code, response.text)

        return result


    # +++ public +++

    requiredAttributes = [
        'offer',
    ]

    def __init__(self, obj = BASE_CLOFFER_DETAILS_DICT):
        """
        Create a new CLOffer instance.
        """
        TripleObject.__init__(self, obj)


    @classmethod
    def forID(klass, objID : str, **args) -> object:
        """
        Get the details and merchant locations for an offer.

        Arguments
        ---------
            objID
        A known, valid offer ID

            cardAccountID
        A valid, known card account ID registered with the system

            countryCode
        The 2-letter ISO code for the country (e.g. US, MX, CA)

            latitude
        The Earth latitude in degrees, with a whole and decimal part, e.g.
        40.46; relative to the equator

            longitude
        The Earth longitude in degrees, with a whole and decimal part, e.g.
        -79.92; relative to Greenwich

            postalCode
        The postalCode associated with the cardAccountID

            radius
        The radius, in meters, to find offers with merchants established
        within that distance to the centroid of the postal code

            spec
        A snake_case dictionary with the query request body

            includeLocations
        Set to `True` to include the merchant locations in the response.

        **Important**

        If `spec` is present, it overrides all other arguments used within its
        scope.  This implementation will ignore all other arguments and try to
        fetch the card linked offer details against the `spec` payload.

        Sample spec (incomplete, for illustrative purposes only; see
        documentation for full spec):

        ```
        {
          'proximity_target': {
            'postal_code': '15206',
            'country_code': 'US',
            'radius': 35000
          },
          'card_account_identifier': {
            'card_account_id': 'triple-abc-123'
          }
        }
        ```

        Returns
        -------
            CLOfferDetails
        An offer details instance if objID is valid, else `None`.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the 
        **`coronado.exceptions`** module.
        """
        if 'spec' in args:
            # Uses spec, backward compatibility; new implementation is for
            # people who don't want to initialize the spec payload (FI
            # requirement).
            return klass._forIDwithSpec(objID, args['spec'], args.get('includeLocations', False))

        requiredArgs = [
            'cardAccountID',
            'countryCode',
            'postalCode',
            'radius',
        ]

        if not all(arg in args.keys() for arg in requiredArgs):
            missing = set(requiredArgs)-set(args.keys())
            raise CallError('argument%s %s missing during instantiation' % ('' if len(missing) == 1 else 's', missing))

        spec = {
            'proximity_target': {
                'postal_code': args['postalCode'],
                'country_code': args['countryCode'],
                'radius': args['radius'],
            },
            'card_account_identifier': {
                'card_account_id': args['cardAccountID'],
            },
        }

        return klass._forIDwithSpec(spec, args.get('includeLocations', False))


    @classmethod
    def create(klass, spec: dict) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def byID(klass, objID: str) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def updateWith(klass, objID: str, spec: dict) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def list(klass, paraMap = None, **args) -> list:
        """
        **Disabled for this class.**
        """
        None




class CardLinkedOffer(Offer):
    """
    CLOffer presents a detailed view of a card linked offer (CLO) with all the
    relevant details.

    Offer objects represent offers from brands and retaliers linked to a payment
    provider like a debit or credit card.  The offer is redeemed by the consumer
    when the linked payment card is used at a point-of-sale.  Offer instances 
    connect on-line advertising campaings with concrete purchases.
    """

    requiredAttributes = [
        'activationRequired',
        'currencyCode',
        'effectiveDate',
        'headline',
        'isActivated',
        'minimumSpend',
# TODO:  internal ticket M-906
#         'mode',
#         'rewardType',
        'type',
    ]

    def __init__(self, obj = BASE_CLOFFER_DETAILS_DICT):
        """
        Create a new OfferSearchResult instance.  Objects of this class should
        not be instantiated via constructor in most cases.  Use the `forQuery()`
        method to query the system for valid results.
        """
        TripleObject.__init__(self, obj)


    @classmethod
    def create(klass, spec: dict) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def byID(klass, objID: str) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def updateWith(klass, objID: str, spec: dict) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def list(klass, paraMap = None, **args) -> list:
        """
        **Disabled for this class.**
        """
        None


class MerchantLocation(TripleObject):
    """
    A merchant's business adddress, whether physical or on-line.

    See `coronado.address.Address`
    """

    requiredAttributes = [
        'address',
        'isOnline',
    ]

    def __init__(self, obj = BASE_CLOFFER_DETAILS_DICT):
        """
        Create a new MerchantLocation instance.
        """
        TripleObject.__init__(self, obj)


    @classmethod
    def create(klass, spec: dict) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def byID(klass, objID: str) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def updateWith(klass, objID: str, spec: dict) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def list(klass, paraMap = None, **args) -> list:
        """
        **Disabled for this class.**
        """
        None

