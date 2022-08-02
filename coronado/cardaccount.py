# vim: set fileencoding=utf-8:


from coronado import TripleEnum
from coronado import TripleObject
from coronado.baseobjects import BASE_CARD_ACCOUNT_DICT
from coronado.exceptions import CallError
from coronado.exceptions import errorFor

import json

import requests


SERVICE_PATH = 'partner/card-accounts'
"""
The default service path associated with CardAccount operations.

Usage:

```
CardAccount.initialize(serviceURL, SERVICE_PATH, auth)
```

Users are welcome to initialize the class' service path from regular strings.
This constant is defined for convenience.
"""


# *** clases and objects ***

class CardAccountStatus(TripleEnum):
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
    def list(klass : object, paramMap = None, **args) -> list:
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
        response = super().list(paramMap, **args)
        result = [ TripleObject(obj) for obj in json.loads(response.content)['card_accounts'] ]
        return result


    @classmethod
    def offerActivations(klass, **args) -> list:
    # def activations(cardAccountID: str, cardAccountExternalID: str = None, cardProgramExternalID = None, publisherID = None, includeExpired = False, page: int = 0):
        """
        Get the activated offers associated with a cardAccountID.

        Arguments
        ---------
            cardAccountID : str
        A triple-defined ID for the entity.

            cardAccountExternalID : str
        A partner-provided external ID that identifies the card account

            cardProgramExternalID : str
        A partner-provided external card program ID; optional

            publisherID : str
        A partner-provided external ID for a publisher

            includeExpired: bool
        When `True`, the results include activations up to 90 days old
        for expired offers along with all active offers; default = `False`

            page : int
        A page offset in the activations list; a page contains <= 1,000
        activations

        `cardAccountExternalID`, `cardProgramExternalID`, and `publisherID` are
        ignored if `cardAccountID` is present.  Providing both raises an error.
        If `cardAccountExternalID` is present, program and publisher IDs are
        optional.  All other arguments are optional.

        Returns
        -------
        The offer activation details associated with the card account details in
        the call.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        if not any(arg in args.keys() for arg in ('cardAccountID', 'cardAccountExternalID')):
            raise CallError('Either cardAccountID or cardAccountExternalID must be included in offerActivations() calls')
        if all(arg in args.keys() for arg in ('cardAccountID', 'cardAccountExternalID')):
            raise CallError('Use either cardAccountID or cardAccountExternalID, not both')

        if 'cardAccountID' in args:
            spec = {
                'card_account_id': args['cardAccountID'],
            }
        else:
            spec = {
                'card_account_external_id': args['cardAccountExternalID'],
                'card_program_external_id': args.get('cardProgramExternalID', None),
                'publisher_id': args.get('publisherID', None),
            }

        endpoint = '/'.join([ klass._serviceURL, 'partner/card-accounts.list-activated-offers', ])
        response = requests.request('POST', endpoint, headers = klass.headers, json = spec)

        if response.status_code == 200:
            result = [ klass(offerActivation) for offerActivation in json.loads(response.content)['offerActivation_activations'] ]
        elif response.status_code == 404:
            result = None
        else:
            raise errorFor(response.status_code, response.text)

        return result


    @classmethod
    def activateFor(**args) -> object:
        """
        """
        None

