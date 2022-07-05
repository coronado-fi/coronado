# vim: set fileencoding=utf-8:


from coronado import CoronadoAPIError
from coronado import CoronadoMalformedObjectError
from coronado import CoronadoUnprocessableObjectError
from coronado import TripleObject
from coronado.baseobjects import BASE_CARD_ACCOUNT_DICT

import enum
import json

import requests


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
    def __init__(self, obj = BASE_CARD_ACCOUNT_DICT):
        TripleObject.__init__(self, obj)

        requiredAttributes = ['objID', 'cardProgramID', 'externalID', 'status', 'createdAt', 'updatedAt', ]

        self.assertAll(requiredAttributes)


    @classmethod
    def list(klass : object) -> list:
        """
        Return a list of all card accounts.

        Returns
        -------
        A list of CardAccount objects
        """
        endpoint = '/'.join([CardAccount.serviceURL, 'partner/card-accounts']) # URL fix later
        headers = { 'Authorization': ' '.join([ CardAccount.auth.tokenType, CardAccount.auth.token, ]) }
        response = requests.request('GET', endpoint, headers = headers)
        result = [ TripleObject(obj) for obj in json.loads(response.content)['card_accounts'] ]

        return result


    @classmethod
    def create(klass, accountSpec : dict) -> object:
        """
        Create a new CardAccount object resource.

        Arguments
        ---------
        accountSpec : dict
            A dictionary with the required camel_case (fugly) fields defined in
            https://api.partners.dev.tripleupdev.com/docs#operation/createCardAccount

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
        if not accountSpec:
            raise CoronadoMalformedObjectError

        endpoint = '/'.join([CardAccount.serviceURL, 'partner/card-accounts']) # URL fix later
        headers = { 'Authorization': ' '.join([ CardAccount.auth.tokenType, CardAccount.auth.token, ]) }
        response = requests.request('POST', endpoint, headers = headers, json = accountSpec)

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

