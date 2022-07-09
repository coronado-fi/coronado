# vim: set fileencoding=utf-8:


from coronado import CoronadoAPIError
from coronado import CoronadoDuplicatesDisallowedError
from coronado import CoronadoMalformedObjectError
from coronado import CoronadoUnexpectedError
from coronado import CoronadoUnprocessableObjectError
from coronado import TripleObject
from coronado.baseobjects import BASE_CARD_ACCOUNT_DICT

import enum
import json

import requests


# *** constants ***

_SERVICE_PATH = 'partner/card-accounts'


# *** clases and objects ***

class CardAccountStatus(enum.Enum):
    """
    Account status object.
    See:  https://api.partners.dev.tripleupdev.com/docs#operation/createCardAccount
    """
    CLOSED = 'CLOSED'
    ENROLLED = 'ENROLLED'
    NOT_ENROLLED = 'NOT_ENROLLED'


    def __str__(self) -> str:
        return self.value


class CardAccount(TripleObject):

    requiredAttributes = ['objID', 'cardProgramID', 'externalID', 'status', 'createdAt', 'updatedAt', ]


    def __init__(self, obj = BASE_CARD_ACCOUNT_DICT):
        TripleObject.__init__(self, obj)


    @classmethod
    def list(klass : object, **args) -> list:
        """
        Return a list of card accounts.  The list is a sequential query from the
        beginning of time if no query parameters are passed:

        Arguments
        ---------
            pubExternalID : str
        A publisher external ID
            cardProgramExternalID : str
        A card program external ID
            cardAccountExternalID : str
        A card account external ID

        Returns
        -------
            list
        A list of TripleObjects objects with some card account attributes:

        - `objID`
        - `externalID`
        - `status`
        """
        paramMap = {
            'cardAccountExternalID': 'card_account_external_id',
            'cardProgramExternalID': 'card_program_external_id',
            'pubExternalID': 'publisher_external_id',
        }
        # params = dict([ (paramMap[k], v) for k, v in args.items()]) if args else None
        params = dict([ (paramMap[k], v) for k, v in args.items()])
        endpoint = '/'.join([CardAccount._serviceURL, _SERVICE_PATH]) # URL fix later
        response = requests.request('GET', endpoint, headers = CardAccount.headers, params = params)
        result = [ TripleObject(obj) for obj in json.loads(response.content)['card_accounts'] ]

        return result


    @classmethod
    def create(klass, spec : dict) -> object:
        """
        Create a new CardAccount object resource based on spec.

        spec:

        ```javascript
        {
            'card_program_external_id': 'somethingelse',
            'external_id': 'anotherthing',
            'publisher_external_id': 'something',
            'status': str(CardAccountStatus.ENROLLED),
        }
        ```

        Arguments
        ---------
            spec : dict
        A dictionary with the required fields to create a new account
        object.


        Returns
        -------
            aCardAccount
        An instance of CardAccount with a valid objID

        Raises
        ------
            CoronadoUnprocessableObjectError
        When the payload syntax is correct but the semantics are invalid
            CoronadoAPIError
        When the service endpoint has an error (500 series)
            CoronadoMalformedObjectError
        When the payload syntax and/or semantics are incorrect, or otherwise the method fails
            CoronadoUnexpectedError
        When the underlying API throws an error not covered by this implementation
        """
        if not spec:
            raise CoronadoMalformedObjectError

        endpoint = '/'.join([CardAccount._serviceURL, 'partner/card-accounts']) # URL fix later
        response = requests.request('POST', endpoint, headers = CardAccount.headers, json = spec)

        if response.status_code == 201:
            account = CardAccount(response.text)
        elif response.status_code == 409:
            raise CoronadoDuplicatesDisallowedError(response.text)
        elif response.status_code == 422:
            raise CoronadoUnprocessableObjectError(response.text)
        elif response.status_code >= 500:
            raise CoronadoAPIError(response.text)
        else:
            raise CoronadoUnexpectedError(response.text)

        return account


    @classmethod
    def byID(klass, objID : str) -> object:
        """
        Return the card account associated with objID.

        Arguments
        ---------
            objID : str
        The account ID associated with the resource to fetch

        Returns
        -------
            aCardAccount
        The CardAccount object associated with objID or None

        Raises
        ------
            CoronadoAPIError
        When the service encounters some error
        """
        endpoint = '/'.join([CardAccount._serviceURL, '%s/%s' % (_SERVICE_PATH, objID)]) # URL fix later
        response = requests.request('GET', endpoint, headers = CardAccount.headers)

        if response.status_code == 404:
            result = None
        elif response.status_code == 200:
            result = CardAccount(response.content.decode())
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
            'status': str(CardAccountStatus.ENROLLED),
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

        Raises
        ------
            CoronadoAPIError
        When the service encounters some error
        """
        endpoint = '/'.join([CardAccount._serviceURL, '%s/%s' % (_SERVICE_PATH, objID)]) # URL fix later
        response = requests.request('PATCH', endpoint, headers = CardAccount.headers, json = spec)

        if response.status_code == 404:
            result = None
        elif response.status_code == 200:
            result = CardAccount(response.content.decode())
        else:
            raise CoronadoAPIError(response.text)

        return result

