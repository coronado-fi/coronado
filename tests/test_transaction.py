# vim: set fileencoding=utf-8:



from coronado import TripleObject
from coronado.address import Address
from coronado.exceptions import CallError
from coronado.exceptions import InvalidPayloadError
from coronado.transaction import MatchingStatus
from coronado.transaction import ProcessorMID
from coronado.transaction import SERVICE_PATH
from coronado.transaction import Transaction
from coronado.transaction import TransactionType

import uuid

import pytest

import coronado.auth as auth


# +++ constants +++

KNOWN_ACCT_EXT_ID = 'pnc-card-69-3149b4780d6f4c2fa21fb45d2637efbb'
KNOWN_ACCT_ID = '1270'
KNOWN_CARD_ACCT_EXT_ID = 'pnc-card-69-0b10aa350dec4201be3107f7aca060f2'
KNOWN_CARD_PROG_EXT_ID = 'prog-66'
KNOWN_MCC = '0780'
KNOWN_PUB_EXTERNAL_ID = '0d7c608a3df5'
KNOWN_TRANSACTION_EXTERNAL_ID = 'tx-45ea79791c594059acaef6869977122d'
KNOWN_TRANSACTION_ID = '8088'


# *** globals ***

_config = auth.loadConfig()
_auth = auth.Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'])

Transaction.initialize(_config['serviceURL'], SERVICE_PATH, _auth)


# *** tests ***

def test_MatchingStatus():
    x = MatchingStatus.MATCHED

    assert isinstance(x, MatchingStatus)
    assert str(x) == 'MATCHED'
    assert str(x) == MatchingStatus.MATCHED.value


def test_ProcessorMID():
    x = ProcessorMID.VISA_VSID

    assert isinstance(x, ProcessorMID)
    assert str(x) == 'VISA_VSID'
    assert str(x) == ProcessorMID.VISA_VSID.value


def test_TransactionType():
    x = TransactionType.PURCHASE

    assert isinstance(x, TransactionType)
    assert str(x) == 'PURCHASE'
    assert str(x) == TransactionType.PURCHASE.value


def test_Transaction():
    t = Transaction()

    assert isinstance(t, Transaction)
    assert t.objID

    result = Transaction(KNOWN_TRANSACTION_ID)
    assert isinstance(result, Transaction)

    with pytest.raises(CallError):
        Transaction({ 'bogus': 'test'})
    with pytest.raises(InvalidPayloadError):
        Transaction(None)
    with pytest.raises(InvalidPayloadError):
        Transaction('bogus')


def test_Transaction_create():
    spec = {
        'amount': 41.95,
        'card_account_external_id': KNOWN_CARD_ACCT_EXT_ID,
        'card_bin': '425907',
        'card_last_4': '3301',
        'card_program_external_id': KNOWN_CARD_PROG_EXT_ID,
        'currency_code': 'USD',
        'debit': True,
        'description': 'Miscellaneous crap',
        'external_id': 'tx-%s' % uuid.uuid4().hex,
        'local_date': '2022-07-19',
        'local_time': '09:26:51',
        'merchant_category_code': {
            'code': KNOWN_MCC,
        },
        'merchant_address': {
            'complete_address': Address().complete,
        },
        'publisher_external_id': KNOWN_PUB_EXTERNAL_ID,
        'transaction_type': 'PURCHASE',
        'processor_mid': uuid.uuid4().hex,
        'processor_mid_type': 'VISA_VSID',
    }

    transaction = Transaction.create(spec)
    assert isinstance(transaction, Transaction)
    assert transaction.objID
    assert transaction.amount == 41.95

    with pytest.raises(CallError):
        Transaction.create(None)

    spec['external_id'] = KNOWN_ACCT_EXT_ID
    with pytest.raises(InvalidPayloadError):
        Transaction.create(spec)

    spec['external_id'] = '****'
    with pytest.raises(CallError):
        Transaction.create(spec)


def test_Transaction_list():
    transactions = Transaction.list()

    assert isinstance(transactions, list)

    if len(transactions):
        transaction = transactions[0]
        assert isinstance(transaction, TripleObject)
        assert transaction.objID

    transactions = Transaction.list(cardAccountExternalID = KNOWN_CARD_ACCT_EXT_ID)
    assert transactions[0].matchingStatus == MatchingStatus.NO_ACTIVE_OFFER

    transactions = Transaction.list(cardProgramExternalID = KNOWN_CARD_PROG_EXT_ID)
    assert transactions[0].matchingStatus == MatchingStatus.NO_ACTIVE_OFFER

    # TODO:  Not implemented, no end dates known
#     transactions = Transaction.list(endDate = KNOWN_CARD_PROG_EXT_ID)
#     assert transactions[0].matchingStatus == MatchingStatus.NO_ACTIVE_OFFER

    transactions = Transaction.list(matched = True)
    if len(transactions):
        assert transactions[0].matchingStatus == MatchingStatus.NO_ACTIVE_OFFER

    transactions = Transaction.list(matched = False)
    if len(transactions):
        assert transactions[0].matchingStatus == MatchingStatus.NO_ACTIVE_OFFER

    # TODO:  Not implemented, no start dates known
#     transactions = Transaction.list(startDate = KNOWN_CARD_PROG_EXT_ID)
#     assert transactions[0].matchingStatus == MatchingStatus.NO_ACTIVE_OFFER

    transactions = Transaction.list(transactionExternalID = KNOWN_TRANSACTION_EXTERNAL_ID)
    assert transactions[0].matchingStatus == MatchingStatus.NO_ACTIVE_OFFER


def test_Transaction_byID():
    result = Transaction.byID(KNOWN_TRANSACTION_ID)
    assert isinstance(result, Transaction)

    assert not Transaction.byID({ 'bogus': 'test'})
    assert not Transaction.byID(None)
    assert not Transaction.byID('bogus')


test_Transaction_create()

