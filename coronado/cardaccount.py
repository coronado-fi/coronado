# vim: set fileencoding=utf-8:


from coronado import TripleEnum
from coronado import TripleObject
from coronado.baseobjects import BASE_CARD_ACCOUNT_DICT
from coronado.exceptions import CallError
from coronado.exceptions import errorFor

import inspect
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
    allAttributes = TripleObject(BASE_CARD_ACCOUNT_DICT).listAttributes()


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


    def offerActivations(self, includeExpired: bool = False, page:int = 0) -> list:
        """
        Get the activated offers associated with a cardAccountID.

        Arguments
        ---------
            cardAccountID : str
        A triple-defined ID for the entity.

            includeExpired: bool
        When `True`, the results include activations up to 90 days old
        for expired offers along with all active offers; default = `False`

            page : int
        A page offset in the activations list; a page contains <= 1,000
        activations

        Returns
        -------
            aList : list
        The offer activation details objects associated with the card account
        details in the call.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        spec = {
            'include_expired': includeExpired,
            'page': page,
        }
        frame = inspect.currentframe()
        obj = frame.f_locals[frame.f_code.co_varnames[0]]
        thisMethod = getattr(obj, frame.f_code.co_name)

        endpoint = '/'.join([ self.__class__._serviceURL, self.__class__._servicePath, self.objID, thisMethod.action, ])
        response = requests.request('POST', endpoint, headers = self.__class__.headers, json = spec)

        if response.status_code == 200:
            result = [ self.__class__(offerActivation) for offerActivation in json.loads(response.content)['offerActivation_activations'] ]
        elif response.status_code == 404:
            result = None
        else:
            raise errorFor(response.status_code, response.text)

        return result


    def activateFor(self, offerIDs: list = None, offerCategory: object = None) -> object:
        """
        Activate the offers listed or by category for the receiver.

        Arguments
        ---------
            offerIDs: list
        A list of offer ID strings to activate

            offerCategory: OfferCategory
        An `coronado.offer.OfferCategory` instance.

        Only one of `offerIDs` list or `offerCategory` are required for
        activation.  This call will raise an error if both are provided in the
        same call.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        if offerIDs and offerCategory or not offerIDs and not offerCategory:
            raise CallError('Provide a value for offerIDs or offerCategory, not both set or both None')

        spec = {
            'offer_category': offerCategory,
            'offer_ids': offerIDs,
        }

        frame = inspect.currentframe()
        obj = frame.f_locals[frame.f_code.co_varnames[0]]
        thisMethod = getattr(obj, frame.f_code.co_name)

        endpoint = '/'.join([ self.__class__._serviceURL, self.__class__._servicePath, self.objID, thisMethod.action, ])
        response = requests.request('POST', endpoint, headers = self.__class__.headers, json = spec)

        if response.status_code == 200:
            result = TripleObject(response.content)
        elif response.status_code == 404:
            result = None
        else:
            raise errorFor(response.status_code, response.text)

        return result


CardAccount.activateFor.action = 'offers.activate'
CardAccount.offerActivations.action = 'offers.list-activations'

