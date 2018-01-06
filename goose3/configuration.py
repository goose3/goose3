# -*- coding: utf-8 -*-
"""\
This is a python port of "Goose" orignialy licensed to Gravity.com
under one or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.

Python port was written by Xavier Grangier for Recrutae

Gravity.com licenses this file
to you under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import tempfile

from goose3.text import StopWords
from goose3.parsers import Parser, ParserSoup
from goose3.version import __version__

AVAILABLE_PARSERS = {
    'lxml': Parser,
    'soup': ParserSoup,
}

KNOWN_ARTICLE_CONTENT_PATTERNS = [
    {'attr': 'class', 'value': 'short-story'},
    {'attr': 'itemprop', 'value': 'articleBody'},
    {'attr': 'class', 'value': 'post-content'},
    {'attr': 'class', 'value': 'g-content'},
    {'tag': 'article'},
]


class Configuration(object):

    def __init__(self):
        # What's the minimum bytes for an image we'd accept is,
        # alot of times we want to filter out the author's little images
        # in the beginning of the article
        self._images_min_bytes = 4500

        # set this guy to false if you don't care about getting images,
        # otherwise you can either use the default
        # image extractor to implement the ImageExtractor
        # interface to build your own
        self._enable_image_fetching = True

        # set this valriable to False if you want to force
        # the article language. OtherWise it will attempt to
        # find meta language and use the correct stopwords dictionary
        self._use_meta_language = True

        # default language
        # it will be use as fallback
        # if use_meta_language is set to false, targetlanguage will
        # be use
        self._target_language = 'en'

        # defautl stopwrods class
        self._stopwords_class = StopWords

        # path to your imagemagick convert executable,
        # on the mac using mac ports this is the default listed
        self._imagemagick_convert_path = "/opt/local/bin/convert"

        # path to your imagemagick identify executable
        self._imagemagick_identify_path = "/opt/local/bin/identify"

        # used as the user agent that
        # is sent with your web requests to extract an article
        # self.browser_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2)"\
        #                         " AppleWebKit/534.52.7 (KHTML, like Gecko) "\
        #                         "Version/5.1.2 Safari/534.52.7"
        self._browser_user_agent = 'Goose/%s' % __version__

        # used to provide custom headers (per requests requirements)
        self._http_headers = None

        # used to provide a dictionary of proxies as supported by the requests
        # package
        # self.http_proxies = {
        #   'http': 'http://10.10.1.10:3128',
        #   'https': 'http://10.10.1.10:1080',
        # }
        # (per requests requirements)
        self._http_proxies = None

        # used when custom authentication is needed
        # (per requests requirements)
        self._http_auth = None

        # debug mode
        # enable this to have additional debugging information
        # sent to stdout
        self._debug = False

        # Parser type
        self._available_parsers = list(AVAILABLE_PARSERS.keys())
        self._parser_class = 'lxml'

        # set the local storage path
        # make this configurable
        self._local_storage_path = os.path.join(tempfile.gettempdir(), 'goose')

        # http timeout
        self._http_timeout = 30

        # known context patterns. Goose at first will search context at dom nodes, qualifying these patterns
        self._known_context_patterns = KNOWN_ARTICLE_CONTENT_PATTERNS

        # Strict mode. Generate exceptions on errors instead of swallowing them
        self._strict = True

    @property
    def known_context_patterns(self):
        ''' list: The context patterns to search to find the likely article content

            Note:
                Each entry must be a dictionary with the following keys: `attr` and `value` \
                or just `tag`
        '''
        return self._known_context_patterns

    @known_context_patterns.setter
    def known_context_patterns(self, val):
        ''' val must be a dictionary or list of dictionaries
            e.g., {'attr': 'class', 'value': 'my-article-class'}
                or [{'attr': 'class', 'value': 'my-article-class'},
                    {'attr': 'id', 'value': 'my-article-id'}]
        '''
        if isinstance(val, list):
            self._known_context_patterns.extend(val)
        else:
            self._known_context_patterns.append(val)

    @property
    def strict(self):
        return self._strict

    @strict.setter
    def strict(self, val):
        self._strict = bool(val)

    @property
    def http_timeout(self):
        return self._http_timeout

    @http_timeout.setter
    def http_timeout(self, val):
        self._http_timeout = val

    @property
    def local_storage_path(self):
        return self._local_storage_path

    @local_storage_path.setter
    def local_storage_path(self, val):
        self._local_storage_path = val

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, val):
        self._debug = bool(val)

    @property
    def parser_class(self):
        return self._parser_class

    @parser_class.setter
    def parser_class(self, val):
        self._parser_class = val

    @property
    def available_parsers(self):  # not settable?
        return self._available_parsers

    @property
    def http_auth(self):
        return self._http_auth

    @http_auth.setter
    def http_auth(self, val):
        self._http_auth = val

    @property
    def http_proxies(self):
        return self._http_proxies

    @http_proxies.setter
    def http_proxies(self, val):
        self._http_proxies = val

    @property
    def http_headers(self):
        return self._http_headers

    @http_headers.setter
    def http_headers(self, val):
        self._http_headers = val

    @property
    def browser_user_agent(self):
        return self._browser_user_agent

    @browser_user_agent.setter
    def browser_user_agent(self, val):
        self._browser_user_agent = val

    @property
    def imagemagick_identify_path(self):
        return self._imagemagick_identify_path

    @imagemagick_identify_path.setter
    def imagemagick_identify_path(self, val):
        self._imagemagick_identify_path = val

    @property
    def imagemagick_convert_path(self):
        return self._imagemagick_convert_path

    @imagemagick_convert_path.setter
    def imagemagick_convert_path(self, val):
        self._imagemagick_convert_path = val

    @property
    def stopwords_class(self):
        return self._stopwords_class

    @stopwords_class.setter
    def stopwords_class(self, val):
        self._stopwords_class = val

    @property
    def target_language(self):
        return self._target_language

    @target_language.setter
    def target_language(self, val):
        self._target_language = val

    @property
    def use_meta_language(self):
        return self._use_meta_language

    @use_meta_language.setter
    def use_meta_language(self, val):
        self._use_meta_language = bool(val)

    @property
    def enable_image_fetching(self):
        return self._enable_image_fetching

    @enable_image_fetching.setter
    def enable_image_fetching(self, val):
        self._enable_image_fetching = bool(val)

    @property
    def images_min_bytes(self):
        return self._images_min_bytes

    @images_min_bytes.setter
    def images_min_bytes(self, val):
        self._images_min_bytes = val

    def get_parser(self):
        return AVAILABLE_PARSERS[self.parser_class]
