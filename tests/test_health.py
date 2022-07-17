# vim: set fileencoding=utf-8:


from coronado import TripleObject
from coronado.auth import Auth
from coronado.auth import loadConfig
from coronado.healthmonitor import HealthMonitor
from coronado.healthmonitor import SERVICE_PATH
from coronado.healthmonitor import main


# +++ tests +++

_config = loadConfig()
_auth = Auth(
    _config["tokenURL"], clientID=_config["clientID"], clientSecret=_config["secret"]
)
HealthMonitor.initialize(_config["serviceURL"], SERVICE_PATH, _auth)


def test_HealthMonitor():
    result = HealthMonitor.check()

    assert isinstance(result, TripleObject)
    assert "APIVersion" in result.__dict__


def test_HealthMonitor_main():
    info = main(unitTest=True)

    assert isinstance(info, dict)
    assert "APIVersion" in info
