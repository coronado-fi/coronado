# vim: set fileencoding=utf-8:


from coronado import TripleEnum
from coronado import TripleObject
from coronado.baseobjects import BASE_REWARD_DICT
from coronado import CoronadoAPIError

import json


# +++ constants +++

SERVICE_PATH = '/partner/rewards'
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

class Reward(TripleObject):
    """
    Reward instances represent exchanges between buyers and sellers that 
    may have a linked offer.
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
        TripleObject.__init__(self, obj)


    @classmethod
    def list(klass: object, paramMap = None, **args) -> list:
        """
        List all rewards that match any of the criteria set by the 
        arguments to this method.

        Arguments
        ---------
            status
        A `coronado.reward.RewardStatus` instance.  May be blank for a list of 
        everything.


        Returns
        -------
            list
        A list of Reward objects; can be `None`.
        """
        paramMap = {
            'status': 'status',
        }
        if 'status' in args:
            if not isinstance(args['status'], RewardStatus):
                raise CoronadoAPIError('invalid type for status - use RewardStatus objects')
            args['status'] = str(args['status'])

        response = super().list(paramMap, **args)
        result = [ TripleObject(obj) for obj in json.loads(response.content)['rewards'] ]
#         for t in result:
#             t.matchingStatus = MatchingStatus(t.matchingStatus)
#             t.merchantCategoryCode = MCC(t.merchantCategoryCode)
#             t.merchantAddress = Address(t.merchantAddress)
#             # TODO:  Pending triple API implementation update
#             # t.transactionType = TransactionType(t.transactionType)

        return result


class RewardStatus(TripleEnum):
    DENIED_BY_MERCHANT = 'DENIED_BY_MERCHANT'
    """
    The merchant or content provider denied the reward.  The `Reward.rewardDetails
    field will include information about the denial.
    """

    DISTRIBUTED_TO_CARDHOLDER = 'DISTRIBUTED_TO_CARDHOLDER'
    """
    The publisher has reported that the reward was given to the cardholder.
    """

    DISTRIBUTED_TO_PUBLISHER = 'DISTRIBUTED_TO_PUBLISHER'
    """
    Reward funds have been sent to the publisher.
    """
    
    PENDING_MERCHANT_APPROVAL = 'PENDING_MERCHANT_APPROVAL'
    """
    The transaction awaits for the merchant or content provider to approve or
    deny the reward.
    """

    PENDING_MERCHANT_FUNDING = 'PENDING_MERCHANT_FUNDING'
    """
    The reward was approved and awaits funding by the merchant.
    """

    PENDING_TRANSFER_TO_PUBLISHER = 'PENDING_TRANSFER_TO_PUBLISHER'
    """
    The reward is funded and funds await distribution to the publisher.
    """

    REJECTED = 'REJECTED'
    """
    The transaction did not meet the offer terms.
    """

