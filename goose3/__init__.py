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
import weakref
from tempfile import mkstemp

from goose3.configuration import Configuration
from goose3.crawler import (CrawlCandidate, Crawler)
from goose3.network import NetworkFetcher
# from goose.version import version_info, __version__


class Goose(object):
    """\

    """

    def __init__(self, config=None):
        # Use the passed in configuration if it is of the right type, otherwise
        # use the default as a base
        if isinstance(config, Configuration):
            self.config = config
        else:
            self.config = Configuration()

        # if config was a passed in dict, parse it into the stored configuration
        if isinstance(config, dict):
            for k, v in list(config.items()):
                if hasattr(self.config, k):
                    setattr(self.config, k, v)

        # setup a single network connection
        self.fetcher = NetworkFetcher(self.config)
        self.finalizer = weakref.finalize(self, self.close)

        # we don't need to go further if image extractor or local_storage is not set
        if not self.config.local_storage_path or not self.config.enable_image_fetching:
            return

        # test if config.local_storage_path is a directory
        if not os.path.isdir(self.config.local_storage_path):
            os.makedirs(self.config.local_storage_path)

        if not os.path.isdir(self.config.local_storage_path):
            raise Exception(self.config.local_storage_path +
                            " directory does not seem to exist, "
                            "you need to set this for image processing downloads"
                            )

        # test to write a dummy file to the directory to check is directory is writable
        level, path = mkstemp(dir=self.config.local_storage_path)
        try:
            with os.fdopen(level, "w"):
                pass
            os.remove(path)
        except IOError:
            raise Exception(self.config.local_storage_path +
                            " directory is not writeble, "
                            "you need to set this for image processing downloads"
                            )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        ''' close the connection and any other cleanup required '''
        if self.fetcher != None:
            self.shutdown_network()
        self.finalizer.atexit = False  # turn off the garbage collection close

    def extract(self, url=None, raw_html=None):
        """\
        Main method to extract an article object from a URL,
        pass in a url and get back a Article
        """
        cc = CrawlCandidate(self.config, url, raw_html)
        return self.crawl(cc)

    def shutdown_network(self):
        ''' ensure the connection is closed '''
        self.fetcher.close()
        self.fetcher = None

    def crawl(self, crawl_candidate):
        parsers = list(self.config.available_parsers)
        parsers.remove(self.config.parser_class)
        try:
            crawler = Crawler(self.config, self.fetcher)
            article = crawler.crawl(crawl_candidate)
        except (UnicodeDecodeError, ValueError) as e:
            if parsers:
                self.config.parser_class = parsers[0]
                return self.crawl(crawl_candidate, self.fetcher)
            else:
                raise e
        return article
