# vim: set fileencoding=utf-8:


from coronado import CoronadoMalformedObjectError
from coronado import TripleObject
from coronado.account import CardAccount
from coronado.account import CardAccountStatus
from coronado.auth import Auth
from coronado.auth import Scopes

import pytest

import coronado.auth as auth


# *** globals ***

_config = auth.loadConfig()
_auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scopes.PUBLISHERS)


# *** tests ***

def test_CardAccount_list():
    accounts = CardAccount.list(_config['serviceURL'], _auth)

    assert isinstance(accounts, list)

    account = accounts[0]
    assert isinstance(account, TripleObject)
    assert account.objID


def test_CardAccount_create():
    accountSpec = {
        'card_program_external_id': 'rebates-nation-24',
        # TODO:  file bug for Matt
        # 'external_id': 'PNC-card-69',
        'external_id': 'pnc-card-69',
        'status': CardAccountStatus.ENROLLED.value,
        # TODO:  file bug for Matt
        # 'publisher_external_id': 'PNCBANK',
        'publisher_external_id': 'pncbank',
    }

    with pytest.raises(CoronadoMalformedObjectError):
        CardAccount.create(None, _config['serviceURL'], _auth)
    
    account = CardAccount.create(accountSpec, _config['serviceURL'], _auth)

    assert account
    # TODO:  finish the implementation; handle 422, other errors
    


def test_CardAccount_byID():
    accountID = 'bogusID'

    account = CardAccount.byID(_config['serviceURL'], accountID, _auth)

    assert not account
    


test_CardAccount_create()
# test_CardAccount_byID()

