# Goose3

### ***Current Master Branch***


### Version 3.0.8
* Fix using different `requests` session for each url fetched
    * Added `close` method to the Goose object
* Allow the Goose object to be a context manager
``` python
from goose3 import Goose
with Goose() as g:
    g.extract(url='some-url-here')
```
***NOTE:*** No need to change code as it will attempt to automatically close
the connection on garbage collection
* Configuration object changes
    * Better handling of the `known_context_patterns` configuration
    * Added http_headers configuration option to be passed to `requests`
    * Added http_proxies configuration option to be passed to `requests`
    * Added http_auth configuration option to be passed to `requests`
* Fix base64 image parsing #7

### Version 3.0.7
* Fix installation issue
    * Removed unused/broken regex
    * Include all necessary files
    * Fix failed tests (**most**)
* Resolved relative URL issue #21
* Resolved temporary files not being properly removed #18
* Removed unused dependencies and code to support python 2 #16
* Fix error when using the configuration object to configure goose #14

### Version 3.0.1
* First working version of Goose3!
