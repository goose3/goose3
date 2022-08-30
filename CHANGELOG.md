# Goose3

### Version 3.1.12
* Allow for extra dependencies [see issue #141](https://github.com/goose3/goose3/issues/141)

### Version 3.1.11
* Replace `md5` with a pure python `fnv_1a` non-cryptographic hash [see issue #133](https://github.com/goose3/goose3/issues/133); Thanks [@openbrian](https://github.com/openbrian)

### Version 3.1.10
* Fix for float based timezones [see issue #128](https://github.com/goose3/goose3/issues/128) Thanks [@Vasniktel](https://github.com/Vasniktel)!
* Add `langdetect` dependency to help resolve some edge cases when missing language information causes text to not be pulled. [see issue #106](https://github.com/goose3/goose3/issues/106)

### Version 3.1.9
* Fix for removing site name from title when it is part of the title [see issue #123](https://github.com/goose3/goose3/issues/123)
* Fix parsing encoding string when encoding information is capitalized [see issue #109](https://github.com/goose3/goose3/issues/109)

### Version 3.1.8
* Fixed title being an empty string when the title is the same as the site name [see PR #117](https://github.com/goose3/goose3/pull/117) Thanks [@Pradhvan](https://github.com/Pradhvan)
* Add optional removal of footnotes [see issue #105](https://github.com/goose3/goose3/issues/105)

### Version 3.1.7
* Fixed author configuration [see PR #96](https://github.com/goose3/goose3/pull/96)
* Improve parent node scoring to get more of the correct data [see PR #102](https://github.com/goose3/goose3/pull/102) Thanks [@skruse](https://github.com/skruse)

### Version 3.1.6
* Improved handling of page encoding [see PR #92](https://github.com/goose3/goose3/pull/92)
* Improved author and published date extraction [see PR #93](https://github.com/goose3/goose3/pull/93) Thanks [@timoilya](https://github.com/timoilya)!
* Added additional schema extractors for schema.org parser [see PR #89](https://github.com/goose3/goose3/pull/89)
* Allow for pulling more then the first og:type data for Opengraph [see PR #90](https://github.com/goose3/goose3/pull/90)

### Version 3.1.5
* Added additional date parsing [see PR #71](https://github.com/goose3/goose3/pull/71) Thanks [@dlrobertson](https://github.com/dlrobertson)!
* Added datetime representation of the publish date `publish_datetime_utc` [see issue #72](https://github.com/goose3/goose3/issues/72)
* Fixed mismatch encoding error [see issue #74](https://github.com/goose3/goose3/issues/74)
* Fixed og_type with NoneType error [see issue #81](https://github.com/goose3/goose3/issues/81) Thanks [dust0x](https://github.com/dust0x)!

### Version 3.1.4
* Fix IndexError when title has only an title splitter or is the site name [see issue #59](https://github.com/goose3/goose3/issues/59) Thanks [@dlrobertson](https://github.com/dlrobertson)!
* Retry the calculate_top_node function with the root node if the first pass failed to find an article which may occur if one or more known article patterns are found, but none contain content [see PR #66](https://github.com/goose3/goose3/pull/66) Thanks [@dlrobertson](https://github.com/dlrobertson)!
* Add parsing of schema.org's ReportageNewsArticle tags [see PR #67](https://github.com/goose3/goose3/pull/67) Thanks [@dlrobertson](https://github.com/dlrobertson)!
* Add additional parsing of opengraph tags [see PR #64](https://github.com/goose3/goose3/pull/64) Thanks [@dlrobertson](https://github.com/dlrobertson)!

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
* Update `get_encodings_from_content` to return a string and remove trailing spaces [see PR #35](https://github.com/goose3/goose3/pull/35)
* Remove infinite recursion on parser selection [see PR #39](https://github.com/goose3/goose3/pull/39)
* Document video and image classes
* Re-add remaining image tests

### Version 3.0.9
* Add `soup` as a parser option to use `lxml.html.soupparser` [see issue #27](https://github.com/goose3/goose3/issues/27)
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
* Fix base64 image parsing [see issue #7](https://github.com/goose3/goose3/issues/7)

### Version 3.0.7
* Fix installation issue
    * Removed unused/broken regex
    * Include all necessary files
    * Fix failed tests (**most**)
* Resolved relative URL issue [see issue #21](https://github.com/goose3/goose3/issues/21)
* Resolved temporary files not being properly removed [see issue #18](https://github.com/goose3/goose3/issues/18)
* Removed unused dependencies and code to support python 2 [see issue #16](https://github.com/goose3/goose3/issues/16)
* Fix error when using the configuration object to configure goose [see issue #14](https://github.com/goose3/goose3/issues/14)

### Version 3.0.1
* First working version of Goose3!
