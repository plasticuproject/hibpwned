# hibpwned
A friendly, low-level, fully functional, Python API wrapper for haveibeenpwned.com <br/>
All data sourced from https://haveibeenpwned.com <br/>
Visit https://haveibeenpwned.com/API/v2 to read the Acceptable Use Policy <br/>
for rules regarding acceptable usage of this API. <br/>


## Installation
```
pip install hibpwned
```


## Usage
This module contains the class Pwned with functions: <br/>

searchAllBreaches <br/>
allBreaches <br/>
singleBreach <br/>
dataClasses <br/>
searchPastes <br/>
searchHashes <br/>

All functions return a JSON object containing relevent data, with the exception <br/>
of searchHashes, which returns a string object.

See module DocStrings for function descriptions and parameters <br/>


## Examples
```python
import hibpwned

myApp = hibpwned.Pwned('test@example.com', 'My_App')

myBreaches = myApp.searchAllBreaches()
Breaches = myApp.allBreaches()
adobe = myApp.singleBreach('adobe')
data = myApp.dataClasses()
myPastes = myApp.searchPastes()
myHashes = myApp.searchHashes('21BD1')
```

