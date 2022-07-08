# vim: set fileencoding=utf-8:

"""
Coronado - a Python API wrapper for the <a href='https://api.tripleup.dev/docs' target='_blank'>triple services API</a>.
"""


from copy import deepcopy

from coronado.baseobjects import BASE_CARD_ACCOUNT_IDENTIFIER_DICT
from coronado.baseobjects import BASE_MERCHANT_CATEGORY_CODE_DICT
from coronado.baseobjects import BASE_MERCHANT_LOCATION_DICT
from coronado.baseobjects import BASE_OFFER_ACTIVATION_DICT
from coronado.baseobjects import BASE_OFFER_DICT
from coronado.baseobjects import BASE_OFFER_DISPLAY_RULES_DICT
from coronado.baseobjects import BASE_PUBLISHER_DICT
from coronado.baseobjects import BASE_REWARD_DICT
from coronado.baseobjects import BASE_TRANSACTION_DICT
from coronado.tools import tripleKeysToCamelCase

import json


# *** constants ***

__VERSION__ = '1.0.7'

API_URL = 'https://api.sandbox.tripleup.dev'
CORONADO_USER_AGENT = 'python-coronado/%s' % __VERSION__



# +++ classes and objects +++

class TripleObject(object):
    """
    Abstract class ancestor to all the triple API objects.
    """
    # +++ class variables ++

    _auth = None
    _serviceURL = None


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


    @classmethod
    def initialize(klass, serviceURL : str, auth : object):
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
        klass._serviceURL = serviceURL
        klass._auth = auth


    def assertAll(self, requiredAttributes: list) -> bool:
        """
        Asserts that all the attributes listed in the requiredAttributes list of
        attribute names are presein the final object.  Coronado/triple objects 
        are built from JSON inputs which may or may not include all required
        attributes.  This method ensures they do.

        Arguments:
            requiresAttributes - a list or tuple of string names
        
        Raises:
            CoronadoMalformedObjectError if one or more attributes are missing.
        """
        if requiredAttributes:
            attributes = self.__dict__.keys()
            if not all(attribute in attributes for attribute in requiredAttributes):
                missing = set(requiredAttributes)-set(attributes)
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
    

    @classmethod
    @property
    def headers(klass):
        return {
            'Authorization': ' '.join([ klass._auth.tokenType, klass._auth.token, ]),
            'User-Agent': CORONADO_USER_AGENT,
        }


    # TODO:  Determine if the create(), list(), byID(), etc. methods need to be
    #        declared as abstract here, and/or if they have common return codes
    #        that we could leverage for implementation.  We won't know for sure
    #        until there is more than one working business object.  There may be
    #        enough commonality to float that behavior to the abstract parent
    #        class.
    @classmethod
    def byID(klass, objID : str) -> object:
        """
        Return the triple object associated with objID.

        Arguments
        ---------
            objID : str
        The object ID associated with the resource to fetch

        Returns
        -------
            The object associated with objID or None

        Raises
        ------
            NotImplementedError
        If the caller attempts this method against the
        TripleObject class
        """
        raise NotImplementedError # because abstract


"""
---
## Exrrors
"""

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

