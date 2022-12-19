[![build](https://github.com/plasticuproject/hibpwned/actions/workflows/tests.yml/badge.svg)](https://github.com/plasticuproject/hibpwned/actions/workflows/tests.yml)
[![Python 3.8](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![PyPI version](https://badge.fury.io/py/hibpwned.svg)](https://badge.fury.io/py/hibpwned)
[![Downloads](https://pepy.tech/badge/hibpwned)](https://pepy.tech/project/hibpwned)
[![Coverage Status](https://coveralls.io/repos/github/plasticuproject/hibpwned/badge.svg?branch=master)](https://coveralls.io/github/plasticuproject/hibpwned?branch=master)
[![CodeQL](https://github.com/plasticuproject/hibpwned/actions/workflows/codeql.yml/badge.svg)](https://github.com/plasticuproject/hibpwned/actions/workflows/codeql.yml)
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

search_all_breaches <br/>
all_breaches <br/>
single_breach <br/>
data_classes <br/>
search_pastes <br/>
search_password <br/>
search_hashes <br/>

All functions return a list of JSON objects containing relevent data, with the exception <br/>
of search_password and search_hashes, which returns an integer and a string object, <br/>
respectively. <br/>

See module DocStrings for function descriptions and parameters <br/>


## Examples
```python
import hibpwned

my_app = hibpwned.Pwned("test@example.com", "My_App", "My_API_Key")

my_breaches = my_app.search_all_breaches()
breaches = my_app.all_breaches()
adobe = my_app.single_breach("adobe")
data = my_app.data_classes()
my_pastes = my_app.search_pastes()
password = my_app.search_password("BadPassword")
my_hashes = my_app.search_hashes("21BD1")
```

