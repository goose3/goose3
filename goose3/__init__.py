"""
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
import logging
import os
import weakref
from tempfile import mkstemp
from typing import List, Union

from goose3.article import Article  # noqa: F401
from goose3.configuration import (  # noqa: F401
    ArticleContextPattern,
    Configuration,
    PublishDatePattern,
)
from goose3.crawler import CrawlCandidate, Crawler
from goose3.image import Image  # noqa: F401
from goose3.network import NetworkFetcher
from goose3.video import Video  # noqa: F401

logger = logging.getLogger(__name__)


class Goose:
    """Extract most likely article content and aditional metadata from a URL or previously fetched HTML document

    Args:
        config (Configuration, dict): A configuration file or dictionary representation of the configuration file
    Returns:
        Goose: An instance of the goose extraction object"""

    def __init__(self, config: Union[Configuration, dict] = None):
        # Use the passed in configuration if it is of the right type, otherwise
        # use the default as a base
        if isinstance(config, Configuration):
            self.config = config
        else:
            self.config = Configuration()

        # if config was a passed in dict, parse it into the stored configuration
        if isinstance(config, dict):
            for k, v in config.items():
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
            msg = (
                f"{self.config.local_storage_path} directory does not seem to exist, "
                "you need to set this for image processing downloads"
            )
            raise Exception(msg)

        # test to write a dummy file to the directory to check is directory is writable
        level, path = mkstemp(dir=self.config.local_storage_path)
        try:
            with os.fdopen(level, "w"):
                pass
            os.remove(path)
        except OSError as exc:
            msg = (
                f"{self.config.local_storage_path} directory is not writeble, "
                "you need to set this for image processing downloads"
            )
            raise Exception(msg) from exc

    def __enter__(self):
        """Setup the context manager"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Define what to do when the context manager exits"""
        self.close()

    def close(self):
        """Close the network connection and perform any other required cleanup

        Note:
            Auto closed when using goose as a context manager or when garbage collected"""
        if self.fetcher is not None:
            self.shutdown_network()
        self.finalizer.atexit = False  # turn off the garbage collection close

    def extract(self, url: str = None, raw_html: str = None) -> Article:
        """Extract the most likely article content from the html page

        Args:
            url (str): URL to pull and parse
            raw_html (str): String representation of the HTML page
        Returns:
            Article: Representation of the article contents including other parsed and extracted metadata"""
        if not url and not raw_html:
            raise ValueError("Either url or raw_html should be provided")

        crawl_candidate = CrawlCandidate(self.config, url, raw_html)
        return self.__crawl(crawl_candidate)

    def shutdown_network(self):
        """Close the network connection

        Note:
            Auto closed when using goose as a context manager or when garbage collected"""
        self.fetcher.close()
        self.fetcher = None

    def __crawl(self, crawl_candidate: CrawlCandidate):
        """wrap the crawling functionality"""

        def crawler_wrapper(parser: str, parsers: List[str], crawl_candidate: CrawlCandidate):
            try:
                crawler = Crawler(self.config, self.fetcher)
                article = crawler.crawl(crawl_candidate)
            except (UnicodeDecodeError, ValueError) as ex:
                logger.error("Parser %s failed to parse the content", parser)
                if parsers:
                    parser = parsers.pop(0)  # remove it also!
                    return crawler_wrapper(parser, parsers, crawl_candidate)
                raise ex
            return article

        # use the wrapper
        parsers = list(self.config.available_parsers)
        parsers.remove(self.config.parser_class)
        return crawler_wrapper(self.config.parser_class, parsers, crawl_candidate)
