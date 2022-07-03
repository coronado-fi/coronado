# vim: set fileencoding=utf-8:


from coronado import CoronadoMalformedObjectError
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
    def list(klass : object, serviceURL = None, auth = None) -> list:
        """
        Return a list of all card accounts.

        Arguments
        ---------
        serviceURL : str
            The URL for the triple service API
        auth : coronado.auth.Auth
            An Auth object with a valid OAuth2 token

        Returns
        -------
        A list of CardAccount objects
        """
        endpoint = '/'.join([serviceURL, 'partner/card-accounts']) # URL fix later
        headers = { 'Authorization': ' '.join([ auth.tokenType, auth.token, ]) }
        response = requests.request('GET', endpoint, headers = headers)
        result = [ TripleObject(obj) for obj in json.loads(response.content)['card_accounts'] ]

        return result


    @classmethod
    def create(klass, accountSpec : dict, serviceURL = None, auth = None) -> object:
        """
        Create a new CardAccount object resource.

        Arguments
        ---------
        accountSpec : dict
            A dictionary with the required camel_case (fugly) fields defined in
            https://api.partners.dev.tripleupdev.com/docs#operation/createCardAccount 
        serviceURL : str
            The URL for the triple service API
        auth : coronado.auth.Auth
            An Auth object with a valid OAuth2 token

        """
        if not accountSpec:
            raise CoronadoMalformedObjectError

        endpoint = '/'.join([serviceURL, 'partner/card-accounts']) # URL fix later
        headers = { 'Authorization': ' '.join([ auth.tokenType, auth.token, ]) }
        x = json.dumps(accountSpec)
        response = requests.request('POST', endpoint, headers = headers, json = accountSpec)
        
        if response.status_code != 200:
            raise CoronadoMalformedObjectError(response.text)

        return None


    @classmethod
    def byID(klass, accountID : str, serviceURL = None, auth = None) -> object:
        """
        Return the card account associated with accountID.

        Arguments
        ---------
        accountID : str
            The account ID associated with the resource to fetch
        serviceURL : str
            The URL for the triple service API
        auth : coronado.auth.Auth
            An Auth object with a valid OAuth2 token

        Returns
        -------
            The CardAccount object associated with accountID or None
        """
        endpoint = '/'.join([serviceURL, 'partner/card-accounts/%s' % accountID]) # URL fix later
        # TODO:  Refactor this in a separate private class method:
        headers = { 'Authorization': ' '.join([ auth.tokenType, auth.token, ]) }
        response = requests.request('GET', endpoint, headers = headers)
        # result = [ TripleObject(obj) for obj in json.loads(response.content)['card_accounts'] ]
        if response.status_code == 404:
            result = None
        else:
            # TODO:  no data there, can't test yet
            pass

        return result

