# vim: set fileencoding=utf-8:


from coronado import CoronadoMalformedObjectError
from coronado import TripleObject
from coronado.auth import Auth
from coronado.auth import Scopes
from coronado.cardprog import CardProgram

import pytest

import coronado.auth as auth


# *** globals ***

_config = auth.loadConfig()


# +++ tests +++

def test_CardProgram_create():
    auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scopes.PUBLISHERS)
    progSpec = {
        # TODO:  Verify the that the camelCase converter deals with BINs 
        'card_bins': [ '425907', '511642', '486010', ],
        'external_id': 'prog-66',
        'name': 'Mojito Rewards',
        'program_currency': 'USD',
        'publisher_external_id': 'pncbank',
    }
    
    with pytest.raises(CoronadoMalformedObjectError):
        CardProgram.create(None, _config['serviceURL'], auth)

    program = CardProgram.create(progSpec, _config['serviceURL'], auth)

    assert program


test_CardProgram_create()

