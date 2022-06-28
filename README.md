% coronado(3) Version 1.0.1 | triple API Python wrapper


Name
====

**coronado** - Python wrapper for the triple API.  The triple API enables
partners to integrate with the triple platform.  The full API documentation is
available from https://api.partners.dev.tripleupdev.com/docs


Synopsis
========

UNDER CONSTRUCTION
| **coronado** _description_ followed by infos


Description
===========

Reference implementation wrapper for the triple API.  All wrappers are
implemented under the umbrella project Coronado, can can be viewed on-line at:

- https://github.com/coronado-fi
- https://coronado.fi - under construction

Use of this API requires credentials issued by tripleup.com and access to an S3
bucket provided by them.  Your client engagement manager can assist you in
setting up access.


Installation
============

The coronado package is available in PyPI.

```bash
pip install coronado
```

This makes the triple API modules available in the current Python environment.
You may verify this with the command:

```bash
pip list | awk 'NR < 3 { print; next; } /coronado/'
```


Authentication
--------------
This component requires OAuth2 with a client ID and client secret.  Please
contact triple to get this information.


Bugs
====

See GitHub issues:  https://github.com/coronado-fi/coronado/issues


Files
=====

- `$HOME/blah/meh/config.json


Author
======
numo LLC and triple LLC, <coronado.project AT numo.com>


See also
========
Section left intentionally blank for release 1.0.0

