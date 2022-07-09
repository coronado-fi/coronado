# vim: set fileencoding=utf-8:


from coronado import TripleObject
from coronado.baseobjects import BASE_CARD_PROGRAM_DICT

import json


# *** constants ***

SERVICE_PATH = 'partner/card-programs'
"""
The default service path associated with CardProgram operations.

Usage:

```
CardProgram.initialize(serviceURL, SERVICE_PATH, auth)
```

Users are welcome to initialize the class' service path from regular strings.
This constant is defined for convenience.
"""


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

    requiredAttributes = ['externalID', 'name', 'programCurrency', ]


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


    @classmethod
    def list(klass : object) -> list:
        """
        Return a list of card programs.

        Returns
        -------
            list
        A list of CardProgram objects
        """
        response = super().list()
        result = [ TripleObject(obj) for obj in json.loads(response.content)['card_programs'] ]

        return result

