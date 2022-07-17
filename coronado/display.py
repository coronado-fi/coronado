# vim: set fileencoding=utf-8:


from coronado import CoronadoAPIError
from coronado import CoronadoMalformedObjectError
from coronado import CoronadoUnexpectedError
from coronado import CoronadoUnprocessableObjectError
from coronado import TripleObject
from coronado.address import Address
from coronado.baseobjects import BASE_CLOFFER_DETAILS_DICT
from coronado.baseobjects import BASE_OFFER_SEARCH_RESULT_DICT
from coronado.merchant import MerchantCategoryCode as MCC
from coronado.offer import Offer
from coronado.offer import OfferCategory
from coronado.offer import OfferDeliveryModes
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
        elif response.status_code == 422:
            raise CoronadoUnprocessableObjectError(response.text)
        elif response.status_code >= 500:
            raise CoronadoAPIError(response.text)
        else:
            raise CoronadoUnexpectedError(response.text)

        return result


    # *** public ***

    requiredAttributes = [
        'objID',
        'activationRequired',
        'currencyCode',
        'effectiveDate',
# TODO:  Bug!
#         'expirationDate',
        'externalID',
        'headline',
        'isActivated',
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
    def forQuery(klass, spec : dict) -> list:
        """
        DEPRECATED
        ----------
        Use `queryWith(objID, spec = spec)` instead.
        """
        return klass.queryWith(spec = spec)


    @classmethod
    def queryWith(klass, **args):
        """
        Search for offers that meet the query search criteria.  The underlying
        service allows for parameterized search and plain text searches.  The
        **<a href='https://api.tripleup.dev/docs' target='_blank'>Search Offers</a>**
        endpoint offers a full description of the object search capabilities.

        Arguments
        ---------
            spec
        A snake_case dictionary with the query request body.

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
            CoronadoUnprocessableObjectError
        When the query `spec` is malformed, missing required fields, or has
        invalid or out of range query parameter values.

            CoronadoAPIError
        When the underlying service is unable to serve the response.  The text 
        in the exception explains the possible reason.

            CoronadoUnexpectedError
        When this object implementation is unable to handle a server response 
        error not covered by existing exceptions.
        """
        if 'spec' in args:
            # Uses spec, backward compatibility; new implementation is for
            # people who don't want to initialize the spec payload (FI
            # requirement).
            return klass._queryWith(args['spec'])

        requiredArgs = [
            'cardAccountID',
            'countryCode',
            'filterOfferType', # filters aren't required; fix later
            'filterCategory',
            'filterLocation',
            'pageOffset',
            'pageSize',
            'postalCode',
            'radius',
            'textQuery',
        ]

        if not all(arg in args.keys() for arg in requiredArgs):
            missing = set(requiredArgs)-set(args.keys())
            raise CoronadoAPIError('argument%s %s missing during instantiation' % ('' if len(missing) == 1 else 's', missing))

        # TODO: Implement arguments and unit test!
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
        raise CoronadoMalformedObjectError('offer attribute not found')

    offer = CardLinkedOffer(d['offer'])
    offer.merchantCategoryCode = MCC(offer.merchantCategoryCode)
    # TODO: the category attribute is missing from the result
    # offer.category = OfferCategory(offer.category)
    # TODO: the rewardType attribute is missing from the result
    # offer.rewardType = OfferCategory(offer.rewardType)
    offer.tripleCategoryName = OfferCategory(offer.tripleCategoryName)
    offer.offerMode = OfferDeliveryModes(offer.offerMode)
    offer.type = OfferType(offer.type)

    merchantLocations = [ MerchantLocation(l) for l in d['merchant_locations'] ]

    for location in merchantLocations:
        location.address = Address(location.address)

    d['offer'] = offer
    d['merchant_locations'] = merchantLocations

    offerDetails = CardLinkedOfferDetails(d)

    return offerDetails


class CardLinkedOfferDetails(Offer):
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
        elif response.status_code == 422:
            raise CoronadoUnprocessableObjectError(response.text)
        elif response.status_code >= 500:
            raise CoronadoAPIError(response.text)
        else:
            raise CoronadoUnexpectedError(response.text)

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
            CoronadoAPIError
        When the underlying service is unable to serve the response.  The text 
        in the exception explains the possible reason.

            CoronadoUnexpectedError
        When this object implementation is unable to handle a server response 
        error not covered by existing exceptions.

            CoronadoUnprocessableObjectError
        When the `spec` query is missing one or more atribute:value pairs.
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
            raise CoronadoAPIError('argument%s %s missing during instantiation' % ('' if len(missing) == 1 else 's', missing))

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

