Goose3 - Article Extractor
===============================================

.. image:: https://img.shields.io/badge/license-Apache_2.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0/
    :alt: License
.. image:: https://github.com/goose3/goose3/workflows/Python%20package/badge.svg?branch=master
    :target: https://github.com/goose3/goose3/actions?query=workflow%3A%22Python+package%22
    :alt: Build Status
.. image:: https://img.shields.io/github/release/goose3/goose3.svg
    :target: https://github.com/goose3/goose3/releases
    :alt: GitHub release
.. image:: https://codecov.io/gh/goose3/goose3/branch/master/graph/badge.svg?token=PoWLaCLbW1
    :target: https://codecov.io/gh/goose3/goose3
    :alt: Test Coverage
.. image:: https://badge.fury.io/py/goose3.svg
    :target: https://badge.fury.io/py/goose3
    :alt: PyPi Release
.. image:: http://pepy.tech/badge/goose3
    :target: http://pepy.tech/count/goose3
    :alt: Downloads

Intro
--------------------------------------------------------------------------------

Goose was originally an article extractor written in Java that has most
recently (Aug2011) been converted to a `scala project <https://github.com/GravityLabs/goose>`_.

This is a complete rewrite in Python. The aim of the software is to
take any news article or article-type web page and not only extract what
is the main body of the article but also all meta data and most probable
image candidate.

Goose will try to extract the following information:

-  Main text of an article
-  Main image of article
-  Any YouTube/Vimeo movies embedded in article
-  Meta Description
-  Meta tags

The Python version was originally rewritten by:

-  Xavier Grangier

Licensing
--------------------------------------------------------------------------------

If you find Goose useful or have issues please drop me a line. I'd love
to hear how you're using it or what features should be improved.

Goose is licensed by Gravity.com under the Apache 2.0 license; see the
LICENSE file for more details.

On-line Documentation
--------------------------------------------------------------------------------
On-line documentation is available on
`Read the Docs <https://goose3.readthedocs.io>`_ which contains more in-depth
documentation.

Setup
--------------------------------------------------------------------------------

To install using pip:

.. code-block::

    pip install goose3

To install from source:

.. code-block::

    mkvirtualenv --no-site-packages goose3
    git clone https://github.com/goose3/goose3.git
    cd goose3
    pip install -r ./requirements/python
    python setup.py install

Take it for a spin
--------------------------------------------------------------------------------

.. code-block:: python

    >>> from goose3 import Goose
    >>> url = 'http://edition.cnn.com/2012/02/22/world/europe/uk-occupy-london/index.html?hpt=ieu_c2'
    >>> g = Goose()
    >>> article = g.extract(url=url)
    >>> article.title
    u'Occupy London loses eviction fight'
    >>> article.meta_description
    "Occupy London protesters who have been camped outside the landmark St. Paul's Cathedral for the past four months lost their court bid to avoid eviction Wednesday in a decision made by London's Court of Appeal."
    >>> article.cleaned_text[:150]
    (CNN) - Occupy London protesters who have been camped outside the landmark St. Paul's Cathedral for the past four months lost their court bid to avoi
    >>> article.top_image.src
    http://i2.cdn.turner.com/cnn/dam/assets/111017024308-occupy-london-st-paul-s-cathedral-story-top.jpg

Configuration
--------------------------------------------------------------------------------

There are two ways to pass configuration to goose. The first one is to
pass goose a Configuration() object. The second one is to pass a
configuration dict.

For instance, if you want to change the userAgent used by Goose just
pass:

.. code-block:: python

    >>> g = Goose({'browser_user_agent': 'Mozilla'})

Switching parsers: Goose can now be used with lxml html parser or lxml
soup parser. By default the html parser is used. If you want to use the
soup parser pass it in the configuration dict :

.. code-block:: python

    >>> g = Goose({'browser_user_agent': 'Mozilla', 'parser_class':'soup'})

One can also set Goose to be more lenient on network exceptions. To turn off
throwing all network exceptions, set the strict configuration setting to false:

.. code-block:: python

    >>> g = Goose({'strict': False})


To turn on image fetching, one can simply enable it using the enable_image_fetching
configuration property:

.. code-block:: python

    >>> g = Goose({'enable_image_fetching': True})


Goose is now language aware
--------------------------------------------------------------------------------

For example, scraping a Spanish content page with correct meta language
tags:

.. code-block:: python

    >>> from goose3 import Goose
    >>> url = 'http://sociedad.elpais.com/sociedad/2012/10/27/actualidad/1351332873_157836.html'
    >>> g = Goose()
    >>> article = g.extract(url=url)
    >>> article.title
    u'Las listas de espera se agravan'
    >>> article.cleaned_text[:150]
    u'Los recortes pasan factura a los pacientes. De diciembre de 2010 a junio de 2012 las listas de espera para operarse aumentaron un 125%. Hay m\xe1s ciudad'

Some pages don't have correct meta language tags, you can force it using
configuration :

.. code-block:: python

    >>> from goose3 import Goose
    >>> url = 'http://www.elmundo.es/elmundo/2012/10/28/espana/1351388909.html'
    >>> g = Goose({'use_meta_language': False, 'target_language':'es'})
    >>> article = g.extract(url=url)
    >>> article.cleaned_text[:150]
    u'Importante golpe a la banda terrorista ETA en Francia. La Guardia Civil ha detenido en un hotel de Macon, a 70 kil\xf3metros de Lyon, a Izaskun Lesaka y '

Passing {'use\_meta\_language': False, 'target\_language':'es'} will
forcibly select Spanish.


Video extraction
--------------------------------------------------------------------------------

.. code-block:: python

    >>> import goose3
    >>> url = 'http://www.liberation.fr/politiques/2013/08/12/journee-de-jeux-pour-ayrault-dans-les-jardins-de-matignon_924350'
    >>> g = goose3.Goose({'target_language':'fr'})
    >>> article = g.extract(url=url)
    >>> article.movies
    [<goose.videos.videos.Video object at 0x25f60d0>]
    >>> article.movies[0].src
    'http://sa.kewego.com/embed/vp/?language_code=fr&playerKey=1764a824c13c&configKey=dcc707ec373f&suffix=&sig=9bc77afb496s&autostart=false'
    >>> article.movies[0].embed_code
    '<iframe src="http://sa.kewego.com/embed/vp/?language_code=fr&amp;playerKey=1764a824c13c&amp;configKey=dcc707ec373f&amp;suffix=&amp;sig=9bc77afb496s&amp;autostart=false" frameborder="0" scrolling="no" width="476" height="357"/>'
    >>> article.movies[0].embed_type
    'iframe'
    >>> article.movies[0].width
    '476'
    >>> article.movies[0].height
    '357'


Goose in Chinese
--------------------------------------------------------------------------------

Some users want to use Goose for Chinese content. Chinese word
segmentation is way more difficult to deal with than occidental
languages. Chinese needs a dedicated StopWord analyser that need to be
passed to the config object.

.. code-block:: python

    >>> from goose3 import Goose
    >>> from goose3.text import StopWordsChinese
    >>> url  = 'http://www.bbc.co.uk/zhongwen/simp/chinese_news/2012/12/121210_hongkong_politics.shtml'
    >>> g = Goose({'stopwords_class': StopWordsChinese})
    >>> article = g.extract(url=url)
    >>> print article.cleaned_text[:150]
    香港行政长官梁振英在各方压力下就其大宅的违章建筑（僭建）问题到立法会接受质询，并向香港民众道歉。

    梁振英在星期二（12月10日）的答问大会开始之际在其演说中道歉，但强调他在违章建筑问题上没有隐瞒的意图和动机。

    一些亲北京阵营议员欢迎梁振英道歉，且认为应能获得香港民众接受，但这些议员也质问梁振英有

Goose in Arabic
--------------------------------------------------------------------------------

In order to use Goose in Arabic you have to use the StopWordsArabic
class.

.. code-block:: python

    >>> from goose3 import Goose
    >>> from goose3.text import StopWordsArabic
    >>> url = 'http://arabic.cnn.com/2013/middle_east/8/3/syria.clashes/index.html'
    >>> g = Goose({'stopwords_class': StopWordsArabic})
    >>> article = g.extract(url=url)
    >>> print article.cleaned_text[:150]
    دمشق، سوريا (CNN) - أكدت جهات سورية معارضة أن فصائل مسلحة معارضة لنظام الرئيس بشار الأسد وعلى صلة بـ"الجيش الحر" تمكنت من السيطرة على مستودعات للأسل


Goose in Korean
--------------------------------------------------------------------------------

In order to use Goose in Korean you have to use the StopWordsKorean
class.

.. code-block:: python

    >>> from goose3 import Goose
    >>> from goose3.text import StopWordsKorean
    >>> url='http://news.donga.com/3/all/20131023/58406128/1'
    >>> g = Goose({'stopwords_class':StopWordsKorean})
    >>> article = g.extract(url=url)
    >>> print article.cleaned_text[:150]
    경기도 용인에 자리 잡은 민간 시험인증 전문기업 ㈜디지털이엠씨(www.digitalemc.com).
    14년째 세계 각국의 통신·안전·전파 규격 시험과 인증 한 우물만 파고 있는 이 회사 박채규 대표가 만나기로 한 주인공이다.
    그는 전기전자·무선통신·자동차 전장품 분야에

TODO
--------------------------------------------------------------------------------

-  Video html5 tag extraction
