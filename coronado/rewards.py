# vim: set fileencoding=utf-8:


from coronado import TripleEnum
from coronado import TripleObject
from coronado.baseobjects import BASE_REWARD_DICT

import json


# --- constants ---

SERVICE_PATH = 'partner/rewards'
"""
The default service path associated with Reward operations.

Usage:

```
Reward.initialize(serviceURL, SERVICE_PATH, auth)
```

Users are welcome to initialize the class' service path from regular strings.
This constant is defined for convenience.
"""


# *** classes and objects ***

class RewardStatus(TripleEnum):
    """
    Describes a reward's state of processing.
    """

    # TODO: Where is rewardDetails defined?
    DENIED_BY_MERCHANT = 'DENIED_BY_MERCHANT'
    """
    The merchant or content provider denied the reward.  See rewardDetails.
    """

    DISTRIBUTED_TO_CARDHOLDER = 'DISTRIBUTED_TO_CARDHOLDER'
    """
    The publisher has reported that the reward has been given to the cardholder.
    """

    DISTRIBUTED_TO_PUBLISHER = 'DISTRIBUTED_TO_PUBLISHER'
    """
    Reward funds have been sent to the publisher.
    """

    PENDING_MERCHANT_APPROVAL = 'PENDING_MERCHANT_APPROVAL'
    """
    The transaction is waiting for the merchant or content provider to approve
    or deny the reward.
    """

    PENDING_MERCHANT_FUNDING = 'PENDING_MERCHANT_FUNDING'
    """
    The reward was approved and is pending funding.
    """

    PENDING_TRANSFER_TO_PUBLISHER = 'PENDING_TRANSFER_TO_PUBLISHER'
    """
    The reward is fundend and funds are waiting for distribution to the
    publisher.
    """

    REJECTED = 'REJECTED'
    """
    The transaction did not meet the offer terms.
    """


class Reward(TripleObject):
    """
    A Reward object describes a reward associated with a transaction and whether
    it met the terms or an offer.
    """

    requiredAttributes = [
        'merchantName',
        'offerID',
        'status',
        'transactionAmount',
        'transactionCurrencyCode',
        'transactionDate',
        'transactionID',
    ]

    def __init__(self, obj = BASE_REWARD_DICT):
        """
        Create a new instance of a reward.  `obj` must correspond to a
        valid, existing object ID if it's not a collection or JSON.

        Arguments
        ---------
            obj
        An object used for building a valid reward.  The object can
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
    def list(klass: object, paramMap = None, **args) -> list:
        """
        Return a list of rewards.  The list is a seqwuential query from the
        beginning of time.

        Arguments
        ---------
            status
        Optional RewardStatus value to query for filtering

        Returns
        -------
            list
        A list of Reward objects.  May return `None`.
        """
        paramMap = { 'status': 'status', }
        response = super().list(paramMap, **args)
        result = [ Reward(obj) for obj in json.loads(response.content)['rewards'] ]
        return result

