# vim: set fileencoding=utf-8:

"""
Coronado - a Python API wrapper for the <a href='https://api.tripleup.dev/docs' target='_blank'>triple services API</a>.

<a href='https://github.com/coronado-fi/coronado/blob/dev/resources/classes.png?raw=true' target='_blank'>
    <img src='https://github.com/coronado-fi/coronado/blob/dev/resources/classes.png?raw=true' width='600' alt='click to view full image'>
</a>
"""


from copy import deepcopy

from coronado.tools import tripleKeysToCamelCase

import json
import enum

import requests


# *** constants ***

__VERSION__ = '1.1.12'

API_URL = 'https://api.sandbox.tripleup.dev'
CORONADO_USER_AGENT = 'python-coronado/%s' % __VERSION__



# +++ classes and objects +++

class TripleEnum(enum.Enum):
    """
    TripleEnum extends the standard Enum class to add support
    for pretty printing of the instance's value by overloading
    the `__str__()` method.  It's a convenience class.
    """
    def __str__(self) -> str:
        return str(self.value)


class TripleObject(object):
    """
    Abstract class ancestor to all the triple API objects.
    """
    # +++ class variables ++

    _auth = None
    _servicePath = None
    _serviceURL = None

    requiredAttributes = None
    """
    A list or tuple of attribute names that are required to be present in the
    JSON or `dict` object during object construction.  See the `assertAll`()
    method.

    **NB:** The attribute names _must_ be in camelCase; these refer to the
    object's internal attributes, not the snake_case initialization payload
    in JSON or a `dict`.
    """


    # +++ implementation +++

    # +++ public +++

    def __init__(self, obj = None):
        """
        Create a new instance of a triple object.  `obj` must correspond to a
        valid, existing object ID if it's not a collection or JSON.  The
        constructor only returns a valid object if a subclass is instantiated;
        TripleObject is an abstract class, and passing it an object ID will
        raise an error.

        Arguments
        ---------
            obj
        An object used for building a valid triple object.  The object can
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
        if isinstance(obj, str):
            if '{' in obj:
                d = json.loads(obj)
            else:  # ValueError JSON test is untenable
                try:
                    d = self.__class__.byID(obj).__dict__
                except:
                    raise CoronadoAPIError('invalid object ID')
        elif isinstance(obj, dict):
            d = deepcopy(obj)
        elif isinstance(obj, TripleObject):
            d = deepcopy(obj.__dict__)
        else:
            raise CoronadoMalformedObjectError

        d = tripleKeysToCamelCase(d)

        for key, value in d.items():
            if isinstance(value, (list, tuple)):
                setattr(self, key, [TripleObject(x) if isinstance(x, dict) else x for x in value])
            else:
                setattr(self, key, TripleObject(value) if isinstance(value, dict) else value)

        self.assertAll()


    def assertAll(self) -> bool:
        """
        Asserts that all the attributes listed in the `requiredAttributes` list
        of attribute names are presein the final object.  Coronado/triple
        objects are built from JSON inputs which may or may not include all
        required attributes.  This method ensures they do.

        Returns
        -------
            True if all required attributes are present during initialization

        Raises
        ------
            CoronadoMalformedObjectError if one or more attributes are missing.

        This method either throws the exception or returns True; it's not a true
        Boolean.
        """
        if self.__class__.requiredAttributes:
            attributes = self.__dict__.keys()
            if not all(attribute in attributes for attribute in self.__class__.requiredAttributes):
                missing = set(self.__class__.requiredAttributes)-set(attributes)
                raise CoronadoMalformedObjectError("attribute%s %s missing during instantiation" % ('' if len(missing) == 1 else 's', missing))


    def listAttributes(self) -> dict:
        """
        Lists all the attributes and their type of the receiving object in the form:

            attrName : type

        Returns
        -------
            A dictionary of objects and types
        """
        keys = sorted(self.__dict__.keys())
        result = dict([ (key, str(type(self.__dict__[key])).replace('class ', '').replace("'", "").replace('<','').replace('>', '')) for key in keys ])

        return result


    def asDict(self) -> dict:
        """
        Returns the receiver as a Python dictionary.  The dictionary is a deep
        copy of the receiver's contents, so it can be manipulated without
        affecting the original object.

        Returns
        -------
            aDictionary
        A dictionary mapping of attributes and their states.
        """
        result = deepcopy(self.__dict__)
        # TODO:  If this method proves to be popular/useful, implement recursion
        #        for embedded TripleObject instances.

        return result


    def inSnakeCaseJSON(self) -> str:
        """
        Return a JSON representation of the receiver with the attributes
        written in snake_case format.

        Return
        ------
            string
        A string with a JSON representation of the receiver.

        Raises
        ------
            NotImplementedError
        If the instance doesn't implement the `asSnakeCaseDictionary()`
        method.  Only classes used for building triple API objects
        require that method implementation.
        """
        return json.dumps(self.asSnakeCaseDictionary())


    def asSnakeCaseDictionary(self) -> dict:
        """
        Return a dict representation of the receiver with the attributes
        written in snake_case format.

        Return
        ------
            dict
        A dictionary representation of the receiver.

        Raises
        ------
            NotImplementedError
        If the instance doesn't implement the `asSnakeCaseDictionary()`
        method.  Only classes used for building triple API objects
        require that method implementation.

        Typical implementation (from a TripleObject specialization that
        represents an address-like object):

        ```
        result = {
            'complete_address': self.complete,
            'country_code': self.countryCode,
            'latitude': self.latitude,
            'line_1': self.line1,
            'line_2': self.line2,
            'locality': self.locality,
            'longitude': self.longitude,
            'postal_code': self.postalCode,
            'province': self.province,
        }

        return result
        ```
        """
        raise NotImplementedError('subclasses must implement this if required')


    def __str__(self) -> str:
        """
        Creates a human-readable string representation of the receiver.

        Returns
        -------
            str
        A human-readable string representation of the receiver.
        """
        result = ''
        keys = sorted(self.__dict__.keys())
        longest = max((len(k) for k in keys))
        formatTrunc = '%%-%ds: %%s... <snip>' % longest
        formatFull = '%%-%ds: %%s' % longest

        for k in keys:
            v = self.__dict__[k]
            if isinstance(v, str) and len(v) > 60:
                result = '\n'.join([ result, formatTrunc % (k, v[:60]), ])
            else:
                result = '\n'.join([ result, formatFull % (k, v), ])

        return result


    @classmethod
    def initialize(klass, serviceURL : str, servicePath : str, auth : object):
        """
        Initialize the class to use an appropriate service URL or authentication
        object.

        Arguments
        ---------
        serviceURL
            A string with an https locator pointing at the service top level URL
        auth
            An instance of Auth configured to use the the serviceURL within the
            defined scope
        """
        klass._servicePath = servicePath.strip('/')
        klass._auth = auth
        klass._serviceURL = serviceURL


    @classmethod
    @property
    def headers(klass):
        return {
            'Authorization': ' '.join([ klass._auth.tokenType, klass._auth.token, ]),
            'User-Agent': CORONADO_USER_AGENT,
        }


    @classmethod
    def create(klass, spec : dict) -> object:
        """
        Create a new TripleObject object resource based on spec.

        spec:

        ```python
        {
        }
        ```

        Arguments
        ---------
            spec : dict
        A dictionary with the required fields to create a new tripleObject
        object.


        Returns
        -------
            aTripleObject
        An instance of TripleObject with a valid objID

        Raises
        ------
            CoronadoUnprocessableObjectError
        When the payload syntax is correct but the semantics are invalid
            CoronadoAPIError
        When the service endpoint has an error (500 series)
            CoronadoMalformedObjectError
        When the payload syntax and/or semantics are incorrect, or otherwise the method fails
            CoronadoUnexpectedError
        When the underlying API throws an error not covered by this implementation
        """
        if klass == TripleObject:
            # Don't allow this in the abstract ancestor
            raise NotImplementedError

        if not spec:
            raise CoronadoMalformedObjectError

        endpoint = '/'.join([klass._serviceURL, klass._servicePath ]) # URL fix later
        response = requests.request('POST', endpoint, headers = klass.headers, json = spec)

        if response.status_code == 201:
            tripleObject = klass(response.text)
        elif response.status_code == 409:
            raise CoronadoDuplicatesDisallowedError(response.text)
        elif response.status_code == 422:
            raise CoronadoUnprocessableObjectError(response.text)
        elif response.status_code >= 500:
            raise CoronadoAPIError(response.text)
        else:
            raise CoronadoUnexpectedError(response.text)

        return tripleObject


    @classmethod
    def byID(klass, objID : str) -> object:
        """
        Return the tripleObject associated with objID.

        Arguments
        ---------
            objID : str
        The tripleObject ID associated with the resource to fetch

        Returns
        -------
            aTripleObject
        The TripleObject object associated with objID or None

        Raises
        ------
            CoronadoAPIError
        When the service encounters some error
        """
        endpoint = '/'.join([klass._serviceURL, '%s/%s' % (klass._servicePath, objID)]) # URL fix later
        response = requests.request('GET', endpoint, headers = klass.headers)

        if response.status_code == 404:
            result = None
        elif response.status_code == 200:
            result = klass(response.content.decode())
        else:
            raise CoronadoAPIError(response.text)

        return result


    @classmethod
    def updateWith(klass, objID : str, spec : dict) -> object:
        """
        Update the receiver with new values for the attributes set in spec.

        spec:

        ```
        spec = {
        }
        ```

        Arguments
        ---------
            objID : str
        The TripleObject ID to update

            spec : dict
        A dict object with the appropriate object references:

        - assumed_name
        - address

        The address should be generated using a Coronado Address object and
        then calling its asSnakeCaseDictionary() method

        Returns
        -------
            aTripleObject
        An updated instance of the TripleObject associated with objID, or None
        if the objID isn't associated with an existing resource.

        Raises
        ------
            CoronadoAPIError
        When the service encounters some error
        """
        endpoint = '/'.join([klass._serviceURL, '%s/%s' % (klass._servicePath, objID)]) # URL fix later
        response = requests.request('PATCH', endpoint, headers = klass.headers, json = spec)

        if response.status_code == 404:
            result = None
        elif response.status_code == 200:
            result = klass(response.content.decode())
        else:
            raise CoronadoAPIError(response.text)

        return result


    @classmethod
    def list(klass : object, paramMap = None, **args) -> list:
        """
        Return a list of tripleObjects.  The list is a sequential query from the
        beginning of time if no query parameters are passed:

        Arguments
        ---------
            See concrete class implementations for specific arguments for each
            use case.

        Returns
        -------
            list
        A list of TripleObjects

        Raises
        ------
            CoronadoForbiddenError
        When trying to list items outside of the correct security scope.  See 
        `coronado.auth.Scope` for details.

            CoronadoUnexpectedError
        When the service or the gateway aren't available, or the service path
        isn't available in the underlying service.
        """
        params = None
        if paramMap:
            params = dict([ (paramMap[k], v) for k, v in args.items() ])

        endpoint = '/'.join([ klass._serviceURL, klass._servicePath ])
        response = requests.request('GET', endpoint, headers = klass.headers, params = params)

        if response.status_code == 403 or response.status_code == 401:
            raise CoronadoForbiddenError(response.text)
        elif response.status_code >= 500:
            raise CoronadoUnexpectedError(response.text)

        return response


class CoronadoAPIError(Exception):
    """
    Raised when the API server fails for some reason (HTTP status 5xx)
    and it's unrecoverable.  This error most often means that the
    service itself is misconfigured, is down, or has a serious bug.
    Printing the reason code will display as much information about why
    the service failed as it is available from the API system.
    """

class CoronadoDuplicatesDisallowedError(Exception):
    """
    Raised when trying to create a Coronado/triple object based on an
    object spec that already exists (e.g. the externalID for the object
    is already registered with the service, or its assumed name is
    duplicated).
    """


class CoronadoMalformedObjectError(Exception):
    """
    Raised when instantiating a Coronado object fails.  May also include
    a string describing the cause of the exception.
    """
    pass


class CoronadoForbiddenError(Exception):
    """
    Raised when requesting access to a triple API resource without credentials
    or with credentials with insufficient privileges.
    """


class CoronadoNotFoundError(Exception):
    """
    Raised when performing a search or update operation and the underlying API
    is unable to tie the `objID` to a triple object of the corresponding type.
    """


class CoronadoUnexpectedError(Exception):
    """
    Raised when performning a Coronado API call that results in an
    unknown, unexpected, undocumented, weird AF error that nobody knows
    how it happened.
    """


class CoronadoUnprocessableObjectError(Exception):
    """
    Raised when instantiating a Coronado object fails because the object
    is well-formed but contains semantic or object representation errors.
    """
    pass

