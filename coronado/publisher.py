# vim: set fileencoding=utf-8:


from coronado import CoronadoMalformedObjectError
from coronado import TripleObject
from coronado.baseobjects import BASE_PUBLISHER_DICT

import requests


# *** classes and objects ***

class Publisher(TripleObject):
    def __init__(self, obj = BASE_PUBLISHER_DICT):
        TripleObject.__init__(self, obj)

        requiredAttributes = [ 'objID', 'assumedName', 'address', 'createdAt', 'updatedAt', ]

        self.assertAll(requiredAttributes)


    @classmethod
    def create(klass, publisherSpec : dict, serviceURL = None, auth = None) -> object:
        """
        """
        if not publisherSpec:
            raise CoronadoMalformedObjectError

        endpoint = '/'.join([serviceURL, 'partner/publishers']) # URL fix later
        headers = { 'Authorization': ' '.join([ auth.tokenType, auth.token, ]) }
        response = requests.request('POST', endpoint, headers = headers, json = publisherSpec)
        
        if response.status_code != 200:
            raise CoronadoMalformedObjectError(response.text)

        return None

