# vim: set fileencoding=utf-8:


from coronado import CoronadoAPIError
from coronado import CoronadoMalformedObjectError
from coronado import CoronadoUnexpectedError
from coronado import CoronadoUnprocessableObjectError
from coronado import TripleEnum
from coronado import TripleObject
from coronado.baseobjects import BASE_REWARD_DICT

import json

import requests


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


# --- functions ---

def _assembleDetailsFrom(payload):
    result = json.loads(payload)

    if isinstance(result, dict):
        result = result['ok']
    elif isinstance(result, list):
        result = [ TripleObject(x) for x in result ]

    return result


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
        result = [ Reward(obj) for obj in json.loads(response.content)['rewards'] ]
# TODO: Map the inner objects!
#         for t in result:
#             t.matchingStatus = MatchingStatus(t.matchingStatus)
#             t.merchantCategoryCode = MCC(t.merchantCategoryCode)
#             t.merchantAddress = Address(t.merchantAddress)
#             # TODO:  Pending triple API implementation update
#             # t.transactionType = TransactionType(t.transactionType)

        return result


    @classmethod
    def _action(klass, transactionID: str, offerID: str, notes:str = None, action:str = 'approve') -> object:
        if action not in ( 'approve', 'deny'):
            raise CoronadoUnprocessableObjectError('allowed actions:  approve, deny')

        spec = {
            'transaction_id': transactionID,
            'offer_id': offerID,
        }
        if notes:
            spec['notes'] = notes

        # TODO: This is a legit 422; the others aren't.
        if None == notes and 'deny' == action:
            raise CoronadoMalformedObjectError('notes attribute missing or set to None')

        if '' == notes and 'deny' == action:
            raise CoronadoMalformedObjectError('notes attribute must have some text; empty strings disallowed')

        endpoint = '/'.join([ klass._serviceURL, 'partner/rewards.%s' % action ])
        response = requests.request('POST', endpoint, headers = klass.headers, json = spec)

        if response.status_code == 200:
            result = _assembleDetailsFrom(response.content)
        elif response.status_code == 404:
            result = False
        elif response.status_code == 422:
            # TODO: THIS 404! {"detail":"No reward found for transaction_id \"129\" and offer_id \"bogus-offer-id\"."} 
            # TODO: Decide between these two:
            klass.responseDDT = json.loads(response.text)
            result = False
            # raise CoronadoUnprocessableObjectError(response.text)
        elif response.status_code >= 500:
            raise CoronadoAPIError(response.text)
        else:
            raise CoronadoUnexpectedError(response.text)

        return result


    @classmethod
    def approve(klass, transactionID: str, offerID: str) -> object:
        """
        Transition a reward status from `PENDING_MERCHANT_APPROVAL` to
        `PENDING_MERCHANT_FUNDING`.

        Arguments
        ---------
            transactionID
        The transaction to which the reward applied

            offerID
        The offer associated with the reward

        Returns
        -------
            Boolean || list || str
        A free from object that may contain one of:
        
        - a sequence of TripleObject instances; OR
        - one or more strings; OR
        - a string with an informative message
        - a Boolean value when the operation is successful

        Raises
        ------
            CoronadoAPIError
        When the underlying service is unable to serve the response.  The text 
        in the exception explains the possible reason.

            CoronadoUnexpectedError
        When this object implementation is unable to handle a server response 
        error not covered by existing exceptions.

            CoronadoUnprocessableObjectError
        When the `spec` query is missing one or more atribute:value pairs.
        """
        return klass._action(transactionID, offerID, action = 'approve')
        
        

    @classmethod
    def deny(klass, transactionID: str, offerID: str, notes: str) -> object:
        """
        Transition a reward from PENDING_MERCHANT_APPROVAL to DENIED_BY_MERCHANT 
        status.

        Arguments
        ---------
            transactionID
        The transaction to which the reward applied

            offerID
        The offer associated with the reward

            notes
        Additional information about why the merchant rejected the offer.  This
        field is not intended for display to cardholders.

        Returns
        -------
            Boolean || list || str
        A free from object that may contain one of:
        
        - a sequence of TripleObject instances; OR
        - one or more strings; OR
        - a string with an informative message
        - a Boolean value when a reward is denied successfully

        Raises
        ------
            CoronadoAPIError
        When the underlying service is unable to serve the response.  The text 
        in the exception explains the possible reason.

            CoronadoUnexpectedError
        When this object implementation is unable to handle a server response 
        error not covered by existing exceptions.

            CoronadoUnprocessableObjectError
        When the `spec` query is missing one or more atribute:value pairs.
        """
        return klass._action(transactionID, offerID, notes, action = 'deny')


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

