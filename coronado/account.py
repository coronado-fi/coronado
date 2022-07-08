# vim: set fileencoding=utf-8:


from coronado import CoronadoAPIError
from coronado import CoronadoMalformedObjectError
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
            'status': 'ENROLLED',
        }
        ```

        Arguments
        ---------
            spec : dict
        A dictionary with the required fields to create a new account
        object.


        Returns
        -------
        An instance of CardAccount with a valid objID

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

        endpoint = '/'.join([CardAccount.serviceURL, 'partner/card-accounts']) # URL fix later
        headers = { 'Authorization': ' '.join([ CardAccount.auth.tokenType, CardAccount.auth.token, ]) }
        response = requests.request('POST', endpoint, headers = headers, json = spec)

#         # TODO:  Fix the issues with the service before this can be validated
#         raise NotImplementedError('The underlying API needs to be refactored for this to work')
        
        if response.status_code == 422:
            raise CoronadoUnprocessableObjectError(response.text)
            
        if response.status_code >= 500:
            raise CoronadoAPIError(response.text)

        if response.status_code != 200:
            raise CoronadoMalformedObjectError(response.text)


        return None


    @classmethod
    def byID(klass, accountID : str) -> object:
        """
        Return the card account associated with accountID.

        Arguments
        ---------
        accountID : str
            The account ID associated with the resource to fetch

        Returns
        -------
            The CardAccount object associated with accountID or None
        """
        endpoint = '/'.join([CardAccount.serviceURL, 'partner/card-accounts/%s' % accountID]) # URL fix later
        # TODO:  Refactor this in a separate private class method:
        headers = { 'Authorization': ' '.join([ CardAccount.auth.tokenType, CardAccount.auth.token, ]) }
        response = requests.request('GET', endpoint, headers = headers)
        # result = [ TripleObject(obj) for obj in json.loads(response.content)['card_accounts'] ]
        if response.status_code == 404:
            result = None
        else:
            # TODO:  no data there, can't test yet
            pass

        return result

