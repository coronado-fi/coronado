# vim: set fileencoding=utf-8:


from coronado import CoronadoAPIError
from coronado import CoronadoDuplicatesDisallowedError
from coronado import CoronadoMalformedObjectError
from coronado import CoronadoUnexpectedError
from coronado import CoronadoUnprocessableObjectError
from coronado import TripleObject
from coronado.baseobjects import BASE_PUBLISHER_DICT

import json

import requests


# +++ constants +++

SERVICE_PATH = 'partner/publishers'
"""
The default service path associated with CardAccount operations.

Usage:

```
CardAccount.initialize(serviceURL, SERVICE_PATH, auth)
```

Users are welcome to initialize the class' service path from regular strings.
This constant is defined for convenience.
"""


# *** classes and objects ***

class Publisher(TripleObject):
    """
    Publisher objects are used for managing portfolios of publishers.  Partners
    who manage card programs for multiple publishers may wish to organize them
    into portfolios.  Portfolios allow offer exclusions which may be applied
    across multiple publishers without having to add individual publishers to
    an offer exclusion.
    """

    requiredAttributes = [ 'objID', 'assumedName', 'address', 'createdAt', 'updatedAt', ]


    def __init__(self, obj = BASE_PUBLISHER_DICT):
        """
        Create a new instance of a publisher.  `obj` must correspond to a
        valid, existing object ID if it's not a collection or JSON.

        Arguments
        ---------
            obj
        An object used for building a valid publisher.  The object can
        be one of:

        - A dictionary - a dictionary with instantiation values as described
          in the API documentation
        - A JSON string
        - A triple objectID

        Raises
        ------
            CoronadoAPIError
        If obj represents an objectID and the ID isn't
        associated with a valid object

            CoronadoMalformedError
        If obj format is invalid (non `dict`, non JSON)
        """
        TripleObject.__init__(self, obj)


    @classmethod
    def create(klass, spec : dict) -> object:
        """
        Create a new Publisher instance using the spec.

        spec:

        ```
        spec = {
            'address': address.asSnakeCaseDictionary(),
            'assumed_name': 'Some Company Name',
            'external_id': 'someID',
            'revenue_share': 1.5,
        }
        ```

        Arguments
        ---------
            spec : dict
        A snake_case publisher input as expected by the triple API
        operation:  https://api.partners.dev.tripleupdev.com/docs#operation/createPublisher

        Returns
        -------
        A new Publisher instance

        Raises
        ------
            CoronadoUnprocessableObjectError
        When the payload syntax is correct but the semantics are invalid
            CoronadoAPIError
        When the service endpoint has an error (500 series)
            CoronadoMalformedObjectError
        When the payload syntax and/or semantics are incorrect, or otherwise the method fails
        """
        if not spec:
            raise CoronadoMalformedObjectError

        endpoint = '/'.join([Publisher._serviceURL, SERVICE_PATH]) # URL fix later
        response = requests.request('POST', endpoint, headers = Publisher.headers, json = spec)

        if response.status_code == 201:
            publisher = Publisher(str(response.text))
        elif response.status_code == 409:
            raise CoronadoDuplicatesDisallowedError(response.text)
        elif response.status_code == 422:
            raise CoronadoUnprocessableObjectError(response.text)
        elif response.status_code >= 500:
            raise CoronadoAPIError(response.text)
        else:
            raise CoronadoUnexpectedError(response.text)

        return publisher


    @classmethod
    def list(klass : object) -> list:
        """
        Return a list of publishers.

        Returns
        -------
            list
        A list of Publisher objects
        """
        endpoint = '/'.join([Publisher._serviceURL, SERVICE_PATH]) # URL fix later
        response = requests.request('GET', endpoint, headers = Publisher.headers)
        result = [ TripleObject(obj) for obj in json.loads(response.content)['publishers'] ]

        return result


    @classmethod
    def byID(klass, objID : str) -> object:
        """
        Return the publisher associated with objID.

        Arguments
        ---------
            objID : str
        The account ID associated with the resource to fetch

        Returns
        -------
            a Publisher
        The Publisher object associated with objID or None
        """
        endpoint = '/'.join([Publisher._serviceURL, '%s/%s' % (SERVICE_PATH, objID)]) # URL fix later
        response = requests.request('GET', endpoint, headers = Publisher.headers)

        if response.status_code == 404:
            result = None
        elif response.status_code == 200:
            result = Publisher(response.content.decode())
        else:
            raise CoronadoAPIError(response.text)

        return result


    @classmethod
    def updateWith(klass, objID : str, spec : dict) -> object:
        """
        Update the receiver with a new assumed name or update its address.

        spec:

        ```
        spec = {
            'assumed_name': 'Something Meaningful and New',
            'address': addressObject.asSnakeCaseDictionary(),
        }
        ```

        Arguments
        ---------
            objID : str
        The Publisher ID to update

            spec : dict
        A dict object with the appropriate object references:
        - assumed_name
        - address
        The address should be generated using a Coronado Address object and
        then calling its asSnakeCaseDictionary() method

        Returns
        -------
            a Publisher
        An updated instance of the Publisher associated with objID, or None
        if the objID isn't associated with an existing resource.
        """
        endpoint = '/'.join([Publisher._serviceURL, '%s/%s' % (SERVICE_PATH, objID)]) # URL fix later
        response = requests.request('PATCH', endpoint, headers = Publisher.headers, json = spec)

        if response.status_code == 404:
            result = None
        elif response.status_code == 200:
            result = Publisher(response.content.decode())
        else:
            raise CoronadoAPIError(response.text)

        return result

