
## Welcome!!

Welcome to the goose3 project: a python article parser automation tool. We hope
that you have found the project to be useful. If you are here, you must want to
help out in some way! We are very grateful for any help and support.

### Table Of Contents
* [Contributing](#contributing)
* [Issues and Bug Reports](#issues-and-bug-reports)
* [Enhancement Requets](#enhancements)
* [Submitting Pull Requests](#pull-requests)
* [Testing](#testing)
* [Coding Style](#coding-style)
* [Code Contributors](#code-contributors)

### Contributing

Contributing to open-source software comes in many forms: adding additional
functionality, reporting and/or fixing bugs and defects, and helping maintain
documentation. Any and all forms are welcome!

Below you will find ways to help the project along with notes on how to report
bugs and issues, request enhancements, and issue pull requests.

#### Issues and Bug Reports

If you have found an issue with goose3, please do not hesitate to let us
know! Before submitting an issue or bug report, we ask that you complete a few
cursory items:

* **Review** current bugs to see if your issue has already been reported. If it
has been previously reported, please comment on the original report with any
additional details. This will help the maintainers triage the issue more
quickly.

* **Ensure** that the issue is **not** related to internet connectivity issues.
Please ensure that static HTML files are also not working. These files of
example issues will make finding the root cause of the defect easier.

* **Determine** that the issue is reproducible - a code sample of the issue
will help narrow down the search for the cause of the issue and may lead to a
quicker fix! Also an example HTML file never hurts!

A **great bug report** will consist of the following:

* A descriptive title

* A brief description of the issue

* Description of the expected results

* An code example to reproduce the error. Please use
[Markdown code blocks](https://help.github.com/articles/creating-and-highlighting-code-blocks/)
with syntax highlighting

* The affected version(s) of goose3

#### Enhancements

Enhancements are additional functionality not currently supported by the
goose3 library. Unfortunately, not all enhancements make sense for the
goal of the project. If you have a desired feature, there are a few things you
can do to possibly help get the feature into the goose3 library:

* **Review** to see if the feature has been requested in the past.

    * If it is requested and still open, add your comment as to why you would
    like it.

    * If it was previously requested but closed, you may be interested in why
    it was closed and not implemented. I will try to explain my reasoning for
    not supporting actions as much as possible.

* Add an issue to the
[issue tracker](https://github.com/barrust/mediawiki/issues) and mark it as an
enhancement. A ***great enhancement*** request will have the following
information:

    * A descriptive title

    * A description of the desired functionality: use cases, added benefit to
    the library, etc.

    * A code example, if necessary, to explain how the code would be used

    * A description of the desired results

#### Pull Requests

Pull requests are how you will be able to add new features, fix bugs, or update
documentation in the goose3 library. To create a pull request, you will
first need to fork the repository, make all necessary changes and then create
a pull request. There are a few guidelines for creating pull requests:

* If the PR only changes documentation, please add `[ci skip]` to the commit
message. To learn more, you can [read about skipping integration testing](https://docs.travis-ci.com/user/customizing-the-build#Skipping-a-build)

* Reference ***any and all*** [issues](https://github.com/barrust/mediawiki/issues)
related to the pull request

#### Testing

Each pull request should add or modify the appropriate tests. goose3 uses
the unittest module to support tests and most are currently found in the
`./tests` folder.

* ###### New Feature:
    * Add tests for each variation of the new feature

* ###### Bug Fix
    * Add at least one regression test of an instance that is working to help
    ensure that the bug fix does not cause a new bug

    * Add at least one test to show the corrected outcome from the updated code
    to help ensure that the code works as intended

#### Coding Style

The goose3 project generally follows the
[flake8](https://github.com/PyCQA/flake8) coding style for consistency
and readability. Code that does not comply with flake8 will not be accepted into
the project as-is. All code should adhere to the flake8 coding style standard
where possible.

The goose3 project also uses [pylint](https://www.pylint.org/)
to help identify potential errors, code duplication, and non-pythonic syntax.
Adhering to pylint's results is not strictly required.

To install the [flake8 compliance checker](https://pypi.org/project/flake8/),
you can simply run the following:

```
pip install flake8
```

To test for flake8 compliance, run the following from the root directory:

```
flake8 goose3
```

### Code Contributors:

A special thanks to all the code contributors to goose3!

* [@lababidi](https://github.com/lababidi) (Maintainer)
* [@barrust](https://github.com/barrust) (Maintainer)
* [@nyanshell](https://github.com/nyanshell)
* [@dlrobertson](https://github.com/dlrobertson)
* [@jeffquach](https://github.com/jeffquach)
* [dust0x](https://github.com/dust0x)
* [@timoilya](https://github.com/timoilya)
* [@Pradhvan](https://github.com/Pradhvan)
* [@Vasniktel](https://github.com/Vasniktel)
* [@openbrian](https://github.com/openbrian)
* [@nnick14](https://github.com/nnick14)
