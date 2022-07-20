# vim: set fileencoding=utf-8:



from coronado import CoronadoDuplicatesDisallowedError
from coronado import CoronadoMalformedObjectError
from coronado import CoronadoUnprocessableObjectError
from coronado.transaction import ProcessorMIDType
from coronado.transaction import MatchingStatusType
from coronado.transaction import SERVICE_PATH
from coronado.transaction import Transaction
from coronado.transaction import TransactionType
from coronado.transaction import MatchingStatusType

import uuid

import pytest

import coronado.auth as auth


# +++ constants +++

KNOWN_ACCT_EXT_ID = 'pnc-card-69-3149b4780d6f4c2fa21fb45d2637efbb'
KNOWN_ACCT_ID = '1270'
KNOWN_CARD_PROG_EXT_ID = 'prog-66'
KNOWN_PUB_EXTERNAL_ID = '0d7c608a3df5'
KNOWN_CARD_ACCT_EXT_ID = 'NANANANA'
KNOWN_MCC = 'fjfjfj'


# *** globals ***

_config = auth.loadConfig()
_auth = auth.Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'])

Transaction.initialize(_config['serviceURL'], SERVICE_PATH, _auth)


# *** tests ***

def test_MatchingStatusType():
    x = MatchingStatusType.MATCHED

    assert isinstance(x, MatchingStatusType)
    assert str(x) == 'MATCHED'
    assert str(x) == MatchingStatusType.MATCHED.value


def test_ProcessorMIDType():
    x = ProcessorMIDType.VISA_VSID

    assert isinstance(x, ProcessorMIDType)
    assert str(x) == 'VISA_VSID'
    assert str(x) == ProcessorMIDType.VISA_VSID.value


def test_TransactionType():
    x = TransactionType.PURCHASE

    assert isinstance(x, TransactionType)
    assert str(x) == 'PURCHASE'
    assert str(x) == TransactionType.PURCHASE.value


def test_Transaction():
    t = Transaction()

    assert isinstance(t, Transaction)
    assert t.objID


@pytest.mark.skip("Bugs in underlying implementation")
def test_Transaction_create():
    spec = {
        'publisher_external_id': KNOWN_PUB_EXTERNAL_ID,
        'card_program_external_id': KNOWN_CARD_PROG_EXT_ID,
        'card_account_external_id': KNOWN_CARD_ACCT_EXT_ID,
        'external_id': 'TX-%s' % uuid.uuid4().hex,
        'card_bin': '425907',
        'card_last_4': '3301',
        'local_date': '2022-07-19',
        'local_time': '09:26:51',
        'debit': True,
        'acmount': 41.95,
        'currency_code': 'USD',
        'transaction_type': 'PURCHASE',
        'description': 'Miscellaneous crap',
        'merchant_category_code': {
            'code': KNOWN_MCC,
        },
        'processor_mid': uuid.uuid4().hex,
        'processor_mid_type': 'VISA_VSID',
    }

    account = Transaction.create(spec)
    assert account

    with pytest.raises(CoronadoMalformedObjectError):
        Transaction.create(None)

    spec['external_id'] = KNOWN_ACCT_EXT_ID
    with pytest.raises(CoronadoDuplicatesDisallowedError):
        Transaction.create(spec)

    spec['external_id'] = '****'
    with pytest.raises(CoronadoUnprocessableObjectError):
        Transaction.create(spec)


