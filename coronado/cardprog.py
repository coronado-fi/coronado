# vim: set fileencoding=utf-8:


from coronado import CoronadoAPIError
from coronado import CoronadoMalformedObjectError
from coronado import TripleObject
from coronado.baseobjects import BASE_CARD_PROGRAM_DICT

import requests


# ***

class CardProgram(TripleObject):
    def __init__(self, obj = BASE_CARD_PROGRAM_DICT):
        TripleObject.__init__(self, obj)

        requiredAttributes = ['externalID', 'name', 'programCurrency', ]

        self.assertAll(requiredAttributes)


    @classmethod
    def create(klass, programSpec : dict) -> object:
        """
        """
        if not programSpec:
            raise CoronadoMalformedObjectError

        endpoint = '/'.join([CardProgram.serviceURL, 'partner/card-programs']) # URL fix later
        response = requests.request('POST', endpoint, headers = CardProgram.headers, json = programSpec)
        
        if response.status_code == 422:
            raise CoronadoMalformedObjectError(response.text)
        else:
            raise CoronadoAPIError(response.text)

        return None

