# vim: set fileencoding=utf-8:


from coronado.auth import Auth
from coronado.auth import Scope
from coronado.cardprog import CardProgram
from coronado.cardprog import SERVICE_PATH
from coronado.exceptions import CallError
from coronado.exceptions import InvalidPayloadError

import uuid

import pytest

import coronado.auth as auth


# +++ constants +++

# TODO: Refactor this (and publisher) to use the "latest created"
#       for the known values.
KNOWN_PROG_ID = '8'
KNOWN_PROG_EXT_ID = 'prog-66'
KNOWN_PUB_EXTERNAL_ID = '0d7c608a3df5'


# *** globals ***

_config = auth.loadConfig()
_auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scope.PUBLISHERS)


CardProgram.initialize(_config['serviceURL'], SERVICE_PATH, _auth)


# +++ tests +++

def test_CardProgram_create():
    progSpec = {
        # TODO:  Verify the that the camelCase converter deals with BINs
        'card_bins': [ '425907', '511642', '486010', ],
        'external_id': 'prog-%s' % uuid.uuid4().hex,
        'name': 'Mojito Rewards %s' % uuid.uuid4().hex,
        'program_currency': 'USD',
        'publisher_external_id': KNOWN_PUB_EXTERNAL_ID,
    }

    program = CardProgram.create(progSpec)
    assert program

    with pytest.raises(CallError):
        CardProgram.create(None)

    progSpec['external_id'] = KNOWN_PROG_EXT_ID
    with pytest.raises(InvalidPayloadError):
        CardProgram.create(progSpec)

    progSpec['external_id'] = '****'
    with pytest.raises(CallError):
        CardProgram.create(progSpec)



def test_CardProgram_list():
    result = CardProgram.list()

    assert len(result)

    program = result[0]
    assert program.objID


def test_CardProgram_byID():
    result = CardProgram.byID(KNOWN_PROG_ID)
    assert isinstance(result, CardProgram)

    assert not CardProgram.byID({ 'bogus': 'test'})
    assert not CardProgram.byID(None)
    assert not CardProgram.byID('bogus')


def test_CardProgram_updateWith():
    control = 'OOO Kukla'
    orgName = CardProgram.byID(KNOWN_PROG_ID).name
    payload = { 'name' : control, }
    result = CardProgram.updateWith(KNOWN_PROG_ID, payload)
    assert result.name == control

    # Reset:
    payload['name'] = orgName
    CardProgram.updateWith(KNOWN_PROG_ID, payload)

