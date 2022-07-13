# vim: set fileencoding=utf-8:


from coronado import TripleEnum
from coronado import TripleObject
from coronado.baseobjects import BASE_CARD_ACCOUNT_DICT

import json


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

