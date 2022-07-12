# vim: set fileencoding=utf-8:


from coronado import CoronadoAPIError
from coronado import CoronadoDuplicatesDisallowedError
# from coronado import CoronadoMalformedObjectError
from coronado import CoronadoNotFoundError
from coronado import CoronadoUnexpectedError
from coronado import CoronadoUnprocessableObjectError
from coronado import TripleObject
from coronado.baseobjects import BASE_OFFER_SEARCH_RESULT_DICT
# 
# import enum
import json
# 
import requests


# +++ constants +++

SERVICE_PATH = 'partner/offer-display/search-offers'


# *** classes and objects ***

class OfferSearchResult(TripleObject):
    """
    Offer search result.  Search results objects are only produced
    when executing a call to the `forQuery()` method.  Each result represents 
    an offer recommendation based on the caller's geolocation, transaction
    history, and offer interactions.

    OfferSearchResult objects can't be instantiated by themselves, and are
    always the result from running a query against the triple API.
    """

    
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
    def forQuery(klass, spec):
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
        A list of offer search results.  The list may be empty/zero-length.
        """
        endpoint = '/'.join([ klass._serviceURL, klass._servicePath, ])
        response = requests.request('POST', endpoint, headers = klass.headers, json = spec)

        if response.status_code == 200:
            result = [ klass(offer) for offer in json.loads(response.content)['offers'] ]
        elif response.status_code == 404:
            raise CoronadoNotFoundError(response.text)
        elif response.status_code == 409:
            raise CoronadoDuplicatesDisallowedError(response.text)
        elif response.status_code == 422:
            raise CoronadoUnprocessableObjectError(response.text)
        elif response.status_code >= 500:
            raise CoronadoAPIError(response.text)
        else:
            raise CoronadoUnexpectedError(response.text)

        return result


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


class CLOfferDetails(TripleObject):
    """
    """

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

