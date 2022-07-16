# vim: set fileencoding=utf-8:


from coronado.auth import Auth
from coronado.auth import Scopes
from coronado import TripleObject

import json

import coronado.auth as auth


# +++ constants +++

SERVICE_PATH = 'partner/healthcheck'


# +++ implementation +++

class HealthMonitor(TripleObject):
    """
    Health monitor reports if the API service is healthy and operational.

    Returns
    -------
        TripleObject
    A triple object with these attributes set:
    
    - `APIVersion`
    - `build`


    Raises
    ------
        CoronadoAPIError
    When the service is unavailable because of a fatal runtime condition.
    """
    # requiredAttributes = [ 'APIVersion', 'build', ]

    def __init__(self):
        TripleObject.__init__(self, None)


    @classmethod
    def check(klass) -> object:
        response = super().list()

        return TripleObject(json.loads(response.content))


# --- functions ---

def main(unitTest : bool = False) -> dict:
    """
    Check the triple API service health by reporting the API version, build ID,
    and other information relevant to implementers.

    This function is the main entry point for a script that will be installed to
    `/usr/local/bin/triplchk` or equivalent depending on whether the Coronado
    package was installed in the system wide Python configuraiton or in a
    virtual environment.

    See:  `man 5 coronado` for details.

    Arguments
    ---------
        unitTest
    Set it to True for running it in a unit test.

    Returns
    -------
        dict
    `None` if running standalone, or a dictionary with information useful to
    API developers if running a unit test.
    """
    _config = auth.loadConfig()
    _auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scopes.PUBLISHERS)

    HealthMonitor.initialize(_config['serviceURL'], SERVICE_PATH, _auth)
    check = HealthMonitor.check()

    print('triple API version = %s, build = %s' % (check.APIVersion, check.build))

    if unitTest:
        return check.__dict__

