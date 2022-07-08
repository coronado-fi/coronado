% coronado(5) Version 1.0.8 | triple API Python wrapper


NAME
====

**coronado** - Native language wrapper for the triple API.  The triple API
enables partners to integrate with the triple platform.  The full API
documentation is available from https://api.tripleup.dev/docs

**Python API reference implementation:**

- https://coronado-fi.github.io/coronado

**JVM API:**

- PENDING

**Typescript/JavaScript API:**

- https://coronado-fi.github.io/coronado-js


SYNOPSIS
========

| **coronado** - Auth, TripleObjects, and business objects manipulation API


DESCRIPTION
===========

Reference implementation wrapper for the triple API.  All wrappers are
implemented under the umbrella project Coronado, can can be viewed on-line at:

- https://github.com/coronado-fi
- https://coronado.fi - under construction

Use of this API requires credentials issued by tripleup.com and access to an S3
bucket provided by them.  Contact tripleup.com to assist you in setting up
access.


Installation
------------
The coronado package is available in PyPI, Maven Central, NPM, CRAN, and other
indices and repositories.  Use the corresponding best-practice mechanism to
install.

_Python_

```bash
pip install coronado
```

This makes the triple API modules available in the current Python environment.
You may verify this with the command:

```bash
pip list | awk 'NR < 3 { print; next; } /coronado/'
```

_JVM - Kotlin, Java, Scala_

```
<dependency>
  <groupId>io.github.coronado-fi</groupId>
  <artifactId>coronado-jvm</artifactId>
  <version>0.0.1-SNAPSHOT</version>
  <type>pom</type>
</dependency>

mvn build
```

_Typescript/Javascript_

```
npm install coronado
```


Authentication
--------------
This component requires OAuth2 credentials available from triple - please
contact a triple representative to get this information.  Credentials cover:

- **clientID**
- **clientName**
- **secret**
- **serviceURL** - different URLs for sandbox, staging, production
- **tokenURL** - the OAuth2 service provider

Authentication tokens and service information are stored in the
**coronado.auth.Auth** objects.  API users need only create an instance of Auth
and use it across all services in the corresponding scope.  The Auth object 
guarantees that a valid, current token is always available, regardless of the
OAuth2 expiration policy set.  If the token expires, Auth objects will request
a new token without user or programmer intervention.

General use:

```
auth = Auth( tokenURL,
             clientID = 'somevalue',
             clientSecret = '53cr3+',
             scope = Scopes.PUBLISHERS)
```


API wrappers usage
------------------
This example leverages the Publisher object and service, but the concepts shown
here apply to all the Coronado API business objects.  A better, more detailed
explanation is available via https://github.com/coronado-fi/coronado/quick-start-guide.ipynb
or by running the same notebook in Lucyfer or Jupyter.

```
# Once per run-time, per Coronado class:
Publisher.initialize(serviceURL, auth)

pubsList = Publisher.list()

pubObject = Publisher.byID(42)

assert pubsList[3].assumedName == pubObject.assumedName

print(pubObject.address)
```

All Coronado TripleObject classes and subclasses can be imported into pandas or
Kotlin DataFrame objects straight from the API, without further modifications:

```
import pandas as pd

panel = pd.DataFrame([ publisher.__dict__ for publisher in pubsList ])

panel.index = panel.objID
del(panel['objID'])
```


API reference
-------------
_Under construction_

The API references for all supporte languages are available from:

https://coronado.fi/docs


BUGS
====

See GitHub issues:  https://github.com/coronado-fi/coronado/issues


FILES
=====
Coronado provides a simple configuration service via API that resolves a JSON
configuration file from system-specific, well-known file system locations.  All
paths are assumed to be under a service user in $HOME.


- Linux (XDG): `$HOME/.config/coronado/config.json
- macOS: `$HOME/Application Support/coronado/config.json
- Windows:  TBD

All implementations use the paths resolved by the Python AppDirs object for 
user configuration.


AUTHOR
======
numo LLC and triple LLC, <coronado.project AT numo.com>


SEE ALSO
========
- https://api.tripleup.dev/docs
- https://github.com/coronado-fi/coronado/quick-start-guide.ipynb

