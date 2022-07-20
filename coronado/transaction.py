# vim: set fileencoding=utf-8:


from coronado import TripleEnum
from coronado import TripleObject
from coronado.baseobjects import BASE_TRANSACTION_DICT

import json


SERVICE_PATH = 'partner/transactions'
"""
The default service path associated with Transaction operations.

Usage:

```
Transaction.initialize(serviceURL, SERVICE_PATH, auth)
```

Users are welcome to initialize the class' service path from regular strings.
This constant is defined for convenience.
"""


# +++ classes +++

class MatchingStatusType(TripleEnum):
    HISTORIC_TRANSACTION = 'HISTORIC_TRANSACTION'
    QUEUED = 'QUEUED'
    NOT_APPLICABLE = 'NOT_APPLICABLE'
    NOT_ENROLLED = 'NOT_ENROLLED'
    NO_ACTIVE_OFFER = 'NO_ACTIVE_OFFER'
    MATCHED = 'MATCHED'


class ProcessorMIDType(TripleEnum):
    AMEX_SE_NUMBER = 'AMEX_SE_NUMBER'
    DISCOVER_MID = 'DISCOVER_MID'
    MC_AUTH_ACQ_ID = 'MC_AUTH_ACQ_ID'
    MC_AUTH_ICA = 'MC_AUTH_ICA'
    MC_AUTH_LOC_ID = 'MC_AUTH_LOC_ID'
    MC_CLEARING_ACQ_ID = 'MC_CLEARING_ACQ_ID'
    MC_CLEARING_ICA = 'MC_CLEARING_ICA'
    MC_CLEARING_LOC_ID = 'MC_CLEARING_LOC_ID'
    MERCHANT_PROCESSOR = 'MERCHANT_PROCESSOR'
    NCR = 'NCR'
    VISA_VMID = 'VISA_VMID'
    VISA_VSID = 'VISA_VSID'


class TransactionType(TripleEnum):
    CHECK = 'CHECK'
    DEPOSIT = 'DEPOSIT'
    FEE = 'FEE'
    PAYMENT = 'PAYMENT'
    PURCHASE = 'PURCHASE'
    REFUND = 'REFUND'
    TRANSFER = 'TRANSFER'
    WITHDRAWAL = 'WITHDRAWAL'


class Transaction(TripleObject):
    """
    Transaction instances represent exchanges between buyers and sellers that 
    may have a linked offer.
    """

    requiredAttributes = [
        'amount',
        'cardAccountID',
        'createdAt',
        'currencyCode',
        'debit',
        'description',
        'externalID',
        'localDate',
        'matchingStatus',
        'transactionType',
        'updatedAt',
    ]

    def __init__(self, obj = BASE_TRANSACTION_DICT):
        TripleObject.__init__(self, obj)

