# Goose3

### Current Version (Master)
* Fix IndexError when title has only an title splitter or is the site name [see issue #59](https://github.com/goose3/goose3/issues/48) Thanks [@dlrobertson](https://github.com/dlrobertson)!
* Retry the calculate_top_node function with the root node if the first pass failed to find an article which may occur if one or more known article patterns are found, but none contain content [see PR #66](https://github.com/goose3/goose3/issues/48) Thanks [@dlrobertson](https://github.com/dlrobertson)!



### Version 3.1.3
* Parse headers and include in `cleaned_text`
* Additional Configuration options:
    * Parse Headers: `parse_headers`
    * Parse Lists: `parse_lists`
    * Pretty Lists: `pretty_lists`
* Catch mismatch encoding meta tag and document encoding [see pull request #53](https://github.com/goose3/goose3/pull/53) Thanks [@jeffquach](https://github.com/jeffquach)!

### Version 3.1.2
* Capture lists from text [see issue #48](https://github.com/goose3/goose3/issues/48) Thanks [@polosatyi](https://github.com/polosatyi)!

### Version 3.1.1
* Catch more PIL exceptions [see issue #42](https://github.com/goose3/goose3/issues/42)
* Update opengraph parsing to maintain all information [see issue #45](https://github.com/goose3/goose3/issues/45)

### Version 3.1.0
* Changed configuration to ***not*** pull images by default [see issue #31](https://github.com/goose3/goose3/issues/31)
* Update `get_encodings_from_content` to return a string and remove trailing spaces [#35](https://github.com/goose3/goose3/pull/35)
* Remove infinite recursion on parser selection [#39](https://github.com/goose3/goose3/pull/39)
* Document video and image classes
* Re-add remaining image tests

### Version 3.0.9
* Add `soup` as a parser option to use `lxml.html.soupparser` [#27](https://github.com/goose3/goose3/issues/27)
* Fix an issue with passing the requests session object to the crawler
* Pylint changes
    * Added pylintrc file
    * Updated variable and positional argument names to be more pythonic
    * Fixed line continuation issues
    * Updated variable names when ambiguous
    * Cleaned up class and static methods

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
* Fix base64 image parsing [#7](https://github.com/goose3/goose3/issues/7)

### Version 3.0.7
* Fix installation issue
    * Removed unused/broken regex
    * Include all necessary files
    * Fix failed tests (**most**)
* Resolved relative URL issue [#21](https://github.com/goose3/goose3/issues/21)
* Resolved temporary files not being properly removed [#18](https://github.com/goose3/goose3/issues/18)
* Removed unused dependencies and code to support python 2 [#16](https://github.com/goose3/goose3/issues/16)
* Fix error when using the configuration object to configure goose [#14](https://github.com/goose3/goose3/issues/14)

### Version 3.0.1
* First working version of Goose3!
