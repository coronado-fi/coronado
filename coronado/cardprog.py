# vim: set fileencoding=utf-8:


from coronado import CoronadoAPIError
from coronado import CoronadoDuplicatesDisallowedError
from coronado import CoronadoMalformedObjectError
from coronado import CoronadoUnexpectedError
from coronado import CoronadoUnprocessableObjectError
from coronado import TripleObject
from coronado.baseobjects import BASE_CARD_PROGRAM_DICT

import json

import requests


# *** constants ***

_SERVICE_PATH = 'partner/card-programs'


# ***

class CardProgram(TripleObject):
    """
    Card programs are logical groupings of card accounts.  A card program is 
    often a specific type of card offering by a CardProgram, like a payment card
    associated with its own rewards like miles or cash back.  Card programs may
    also be used for organizing card accounts in arbirtrary groupings.

    Card accounts may not move between card programs, and cannot be represented
    in more than one card program at a time.
    """
    def __init__(self, obj = BASE_CARD_PROGRAM_DICT):
        """
        Create a new instance of a card program.  `obj` must correspond to a
        valid, existing object ID if it's not a collection or JSON.

        Arguments
        ---------
            obj
        An object used for building a valid card program.  The object can
        be one of:

        - A dictionary - a dictionary with instantiation values as described
          in the API documentation
        - A JSON string
        - A triple objectID

        Raises
        ------
            CoronadoAPIError
        If obj represents an objectID and the ID isn't
        associated with a valid object

            CoronadoMalformedError
        If obj format is invalid (non `dict`, non JSON)
        """
        TripleObject.__init__(self, obj)

        requiredAttributes = ['externalID', 'name', 'programCurrency', ]

        self.assertAll(requiredAttributes)


    @classmethod
    def create(klass, spec : dict) -> object:
        """
        Create a new CardProgram instance using the spec.

        spec:

        ```
        spec = {
            'card_bins': [ '425907', '511642', '486010', ],
            'external_id': 'someuniquestring',
            'name': 'Something Meaningful',
            'program_currency': 'USD',
            'publisher_external_id': KNOWN_PUB_EXTERNAL_ID,
        }
        ```

        Arguments
        ---------
            spec : dict
        A snake_case publisher input as expected by the triple API
        operation

        Returns
        -------
            A new CardProgram instance

        Raises
        ------
            CoronadoUnprocessableObjectError
        When the payload syntax is correct but the semantics are invalid

            CoronadoAPIError
        When the service endpoint has an error (500 series)

            CoronadoMalformedObjectError
        When the payload syntax and/or semantics are incorrect, or otherwise the method fails
        """
        if not spec:
            raise CoronadoMalformedObjectError

        endpoint = '/'.join([CardProgram._serviceURL, _SERVICE_PATH]) # URL fix later
        response = requests.request('POST', endpoint, headers = CardProgram.headers, json = spec)
        
        if response.status_code == 201:
            program = CardProgram(response.text)
        elif response.status_code == 409:
            raise CoronadoDuplicatesDisallowedError(response.text)
        elif response.status_code == 422:
            raise CoronadoUnprocessableObjectError(response.text)
        elif response.status_code >= 500:
            raise CoronadoAPIError(response.text)
        else:
            raise CoronadoUnexpectedError(response.text)

        return program


    @classmethod
    def list(klass : object) -> list:
        """
        Return a list of card programs.

        Returns
        -------
            list
        A list of CardProgram objects
        """
        endpoint = '/'.join([CardProgram._serviceURL, _SERVICE_PATH]) # URL fix later
        response = requests.request('GET', endpoint, headers = CardProgram.headers)
        result = [ TripleObject(obj) for obj in json.loads(response.content)['card_programs'] ]

        return result


    @classmethod
    def byID(klass, objID : str) -> object:
        """
        Return the card program associated with objID.

        Arguments
        ---------
        objID : str
            The card program ID associated with the resource to fetch

        Returns
        -------
            The card program object associated with objID or None
        """
        endpoint = '/'.join([CardProgram._serviceURL, '%s/%s' % (_SERVICE_PATH, objID)]) # URL fix later
        response = requests.request('GET', endpoint, headers = CardProgram.headers)

        if response.status_code == 404:
            result = None
        elif response.status_code == 200:
            result = CardProgram(response.content.decode())
        else:
            raise CoronadoAPIError(response.text)

        return result


    @classmethod
    def updateWith(klass, objID : str, spec : dict) -> object:
        """
        Update the receiver with new values for the attributes set in spec.

        spec:

        ```
        spec = {
            'name': 'Something Meaningful and New',
        }
        ```

        Arguments
        ---------
            objID : str
        The CardProgram ID to update

            spec : dict
        A dict object with the appropriate object references:
        
        - assumed_name
        - address

        The address should be generated using a Coronado Address object and
        then calling its asSnakeCaseDictionary() method

        Returns
        -------
            aCardProgram
        An updated instance of the CardProgram associated with objID, or None
        if the objID isn't associated with an existing resource.
        """
        endpoint = '/'.join([CardProgram._serviceURL, '%s/%s' % (_SERVICE_PATH, objID)]) # URL fix later
        response = requests.request('PATCH', endpoint, headers = CardProgram.headers, json = spec)

        if response.status_code == 404:
            result = None
        elif response.status_code == 200:
            result = CardProgram(response.content.decode())
        else:
            raise CoronadoAPIError(response.text)

        return result

