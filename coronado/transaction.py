# vim: set fileencoding=utf-8:


from coronado import TripleEnum
from coronado import TripleObject
from coronado.address import Address
from coronado.baseobjects import BASE_TRANSACTION_DICT
from coronado.merchantcodes import MerchantCategoryCode as MCC

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


    # TODO:  Update the docstring to link to Rewards and reward details when
    #        that code is implemented by the back-end and Coronado.
    @classmethod
    def list(klass: object, paramMap = None, **args) -> list:
        """
        List all transactions that match any of the criteria set by the 
        arguments to this method.

        Arguments
        ---------
            cardAccountExternalID
        String, 1-50 characters partner-provided external ID

            cardProgramExternalID
        String, 1-50 characters partner-provided external ID

            endDate
        A string date - includes only transactions that start from the date in
        format:  YYYY-mm-dd

            matched
        A Boolean flag; if True, includes only the transactions matched to an
        active offer.  See Reward Details for more information.
            publisherExternalID
        String, 1-50 characters partner-provided external ID

            startDate
        A string date - includes only transactions that start from the date in
        format:  YYYY-mm-dd

            transactionExternalID
        String, 1-50 characters partner-provided external ID

        Returns
        -------
            list
        A list of Transaction objects; can be `None`.
        """
        paramMap = {
            'cardAccountExternalID': 'card_account_external_id',
            'cardProgramExternalID': 'card_program_external_id',
            'endDate': 'end_date',
            'matched': 'matched',
            'startDate': 'start_date',
            'transactionExternalID': 'transaction_external_id',
        }
        response = super().list(paramMap, **args)
        result = [ TripleObject(obj) for obj in json.loads(response.content)['transactions'] ]
        for t in result:
            t.matchingStatus = MatchingStatus(t.matchingStatus)
            # TODO: Bug!  Why are there transactions without an MCC?
            if t.merchantCategoryCode:
                t.merchantCategoryCode = MCC(t.merchantCategoryCode)
            # TODO: error!
            # t.merchantAddress = Address(t.merchantAddress)
            # TODO:  Pending triple API implementation update
            # t.transactionType = TransactionType(t.transactionType)

        return result


    @classmethod
    def updateWith(klass, objID: str, spec: dict) -> object:
        """
        **Disabled for this class.**
        """
        None


class MatchingStatus(TripleEnum):
    HISTORIC_TRANSACTION = 'HISTORIC_TRANSACTION'
    QUEUED = 'QUEUED'
    NOT_APPLICABLE = 'NOT_APPLICABLE'
    NOT_ENROLLED = 'NOT_ENROLLED'
    NO_ACTIVE_OFFER = 'NO_ACTIVE_OFFER'
    MATCHED = 'MATCHED'


class ProcessorMID(TripleEnum):
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

