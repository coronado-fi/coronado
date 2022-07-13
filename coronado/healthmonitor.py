# vim: set fileencoding=utf-8:


from coronado.auth import Auth
from coronado.auth import Scopes
from coronado import TripleObject

import json

import coronado.auth as auth


# +++ constants +++

SERVICE_PATH = 'partner/healthcheck'


class HealthMonitor(TripleObject):
    """
    Health monitor.  **NEEDS DOCUMENTATION**
    """
    requiredAttributes = [ 'APIVersion', 'build', ]

    def __init__(self):
        TripleObject.__init__(self, None)


    @classmethod
    def check(klass) -> object:
        response = super().list()

        return TripleObject(json.loads(response.content))


if '__main__' == __name__:
    # TODO:  Turn this into a real object and define its unit tests and a runner.
    _config = auth.loadConfig()
    _auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scopes.PUBLISHERS)

    HealthMonitor.initialize(_config['serviceURL'], SERVICE_PATH, _auth)
    check = HealthMonitor.check()

    print('API version = %s, build = %s' % (check.apiVersion, check.build)) # TODO: fix the camelCase converter

