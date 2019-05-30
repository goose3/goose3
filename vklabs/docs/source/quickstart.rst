.. _quickstart:

Quickstart
===============================================================================


Install
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Goose3 is a python3 fork of the python-goose library. To use goose3, one must
run everything using python3. All python commands assume the usage of the
correct python version.

Using pip
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

The easiest way to install goose3 is to use pip:

::

    $ pip install goose3


From source
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

To install from source simply clone the
`repository on GitHub <https://github.com/goose3/goose3>`__,
then run the following command from the extracted folder:

::

    $ python setup.py install


Setup
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Setting up Goose3 using the standard configuration is fairly straight forward:

::

    from vklabs.goose3 import Goose

    g = Goose()
    article = g.extract(url='http://this-url.html')
    print(article.cleaned_text)
    g.close()

For extracting lots of HTML files or URLs, one can also use it as a context
manager:

::

    from vklabs.goose3 import Goose

    urls = [...]
    with Goose() as g:
        for tmp in urls:
            article = g.extract(url=tmp)
            print(article.cleaned_text)

Setting Config Options
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

One can also alter how goose3 performs the extraction and what items are
extracted by passing a configuration to Goose. There are several ways to set
the configuration options.

For more details on available configuration settings, see :ref:`configdocs`

Use Configuration object
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

::

    from vklabs.goose3 import Goose
    from vklabs.goose3.configuration import Configuration

    config = Configuration()
    config.strict = False  # turn of strict exception handling
    config.browser_user_agent = 'Mozilla 5.0'  # set the browser agent string
    config.http_timeout = 5.05  # set http timeout in seconds

    with Goose(config) as g:
        ...


Use Dictionary
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
One can pass in a dictionary with keys that match the configuration properties
one would like to change:

::

    from vklabs.goose3 import Goose

    config = {}
    config['strict'] = False  # turn of strict exception handling
    config['browser_user_agent'] = 'Mozilla 5.0'  # set the browser agent string
    config['http_timeout'] = 5.05  # set http timeout in seconds

    with Goose(config) as g:
        pass

Or if there are only a few changes:
::

    from vklabs.goose3 import Goose

    with Goose({'http_timeout': 5.0}) as g:
        pass

After Object Creation
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
One can also change configuration options after the Goose object has been
created:

::

    from vklabs.goose3 import Goose

    g = Goose()
    g.config.browser_user_agent = 'Mozilla 5.0'


Configuration Helper Classes
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
For some, more complex configuration options, there are classes available to
help ensure that the correct values are provided. One does not need to use the
provided classes, but it does make things a bit simpler.

::

    from vklabs.goose3 import Goose
    from vklabs.goose3.configuration import Configuration, ArticleContextPattern, PublishDatePattern, AuthorPattern

    config = Configuration()

    # we know of a particular article location in the site we are pulling from
    config.known_context_patterns = ArticleContextPattern(attr="id", value="my-site-article")

    # publish date
    config.known_publish_date_tags = PublishDatePattern(attr="id", value="pubdate", content="content")

    # author
    config.known_author_patterns = AuthorPattern(attr="id", value="writer", content="content")


Reading Results
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Results from the extraction are returned as an Article object. Reading the
desired results is as simple as reading the desired property. The most commonly
asked for property is `cleaned_text` which holds the non-html formatted text of
the extracted article.


For more details and for all available properties, see :ref:`articledocs`

::

    from vklabs.goose3 import Goose

    urls = [...]
    with Goose() as g:
        for tmp in urls:
            article = g.extract(url=tmp)
            print(article.cleaned_text)
