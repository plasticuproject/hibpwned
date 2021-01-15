[![Build Status](https://travis-ci.org/plasticuproject/hibpwned.svg?branch=master)](https://travis-ci.org/plasticuproject/hibpwned)
[![Python 3.7](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![PyPI version](https://badge.fury.io/py/hibpwned.svg)](https://badge.fury.io/py/hibpwned)
[![Downloads](https://pepy.tech/badge/hibpwned)](https://pepy.tech/project/hibpwned)
[![Coverage Status](https://coveralls.io/repos/github/plasticuproject/hibpwned/badge.svg?branch=master)](https://coveralls.io/github/plasticuproject/hibpwned?branch=master)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/plasticuproject/hibpwned.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/plasticuproject/hibpwned/context:python)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=plasticuproject_hibpwned&metric=alert_status)](https://sonarcloud.io/dashboard?id=plasticuproject_hibpwned)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=plasticuproject_hibpwned&metric=security_rating)](https://sonarcloud.io/dashboard?id=plasticuproject_hibpwned)
# hibpwned
A friendly, low-level, fully functional, Python API wrapper for haveibeenpwned.com <br/>
All data sourced from https://haveibeenpwned.com <br/>
Visit https://haveibeenpwned.com/API/v3 to read the Acceptable Use Policy <br/>
for rules regarding acceptable usage of this API. <br/>


## Installation
```
pip install hibpwned
```
Making calls to the HIBP API requires a key. You can purchase an HIBP-API-Key at <br/>
https://haveibeenpwned.com/API/Key


## Usage
This module contains the class Pwned with functions: <br/>

searchAllBreaches <br/>
allBreaches <br/>
singleBreach <br/>
dataClasses <br/>
searchPastes <br/>
searchPassword <br/>
searchHashes <br/>

All functions return a JSON object containing relevent data, with the exception <br/>
of searchPassword and searchHashes, which returns an integer and a string object, <br/>
respectively. <br/>

See module DocStrings for function descriptions and parameters <br/>


## Examples
```python
import hibpwned

myApp = hibpwned.Pwned('test@example.com', 'My_App', 'My_API_Key')

myBreaches = myApp.searchAllBreaches()
Breaches = myApp.allBreaches()
adobe = myApp.singleBreach('adobe')
data = myApp.dataClasses()
myPastes = myApp.searchPastes()
password = myApp.searchPassword('BadPassword')
myHashes = myApp.searchHashes('21BD1')
```

