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
import codecs
import functools
import json
import os
import unittest
from datetime import datetime

import requests_mock

from goose3 import Goose
from goose3.configuration import Configuration
from goose3.version import __version__

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


def load_resource(path):
    try:
        with codecs.open(path, "r", "utf-8") as fobj:
            content = fobj.read()
        return content
    except OSError:
        raise OSError("Couldn't open file %s" % path)


def fail_after(version, method=None):
    """Decorator to add to tests to ensure that they fail if a deprecated
    feature is not removed before the specified version
    Args:
        version (str): The version to check against"""

    def decorator_wrapper(func):
        @functools.wraps(func)
        def test_inner(*args, **kwargs):
            if [int(x) for x in version.split(".")] <= [int(x) for x in __version__.split(".")]:
                msg = "{} is depricated and must be removed by version {}".format(
                    method if method else func.__name__, version
                )
                raise AssertionError(msg)
            return func(*args, **kwargs)

        return test_inner

    return decorator_wrapper


class TestExtractionBase(unittest.TestCase):
    """
    Extraction test case
    """

    # callback = MockResponseExtractors

    def getRawHtml(self):
        test, suite, module, cls, func = self.id().split(".")
        path = os.path.join(
            os.path.dirname(CURRENT_PATH), "data", suite, module.partition("test_")[2], "%s.html" % func
        )
        path = os.path.abspath(path)
        content = load_resource(path)
        return content

    def loadData(self):
        """ """
        full_id = self.id().split(".")

        test, module, cls, func = full_id
        path = os.path.join(
            os.path.dirname(CURRENT_PATH),
            "tests",
            "data",
            # suite,
            module.partition("test_")[2],
            "%s.json" % func,
        )
        path = os.path.abspath(path)
        content = load_resource(path)
        self.data = json.loads(content)

    def loadHtml(self):
        test, module, cls, func = self.id().split(".")
        path = os.path.join(
            os.path.dirname(CURRENT_PATH), "tests", "data", module.partition("test_")[2], "%s.html" % func
        )
        path = os.path.abspath(path)
        self.html = load_resource(path)

    def assert_cleaned_text(self, field, expected_value, result_value):
        # # TODO : handle verbose level in tests
        # print "\n=======================::. ARTICLE REPORT %s .::======================\n" % self.id()
        # print 'expected_value (%s) \n' % len(expected_value)
        # print expected_value
        # print "-------"
        # print 'result_value (%s) \n' % len(result_value)
        # print result_value

        # cleaned_text is Null
        msg = "Resulting article text was NULL!"
        self.assertNotEqual(result_value, None, msg=msg)

        # cleaned_text length
        msg = "Article text was not as long as expected beginning!"
        self.assertTrue(len(expected_value) <= len(result_value), msg=msg)

        # clean_text value
        result_value = result_value[0 : len(expected_value)]
        msg = "The beginning of the article text was not as expected!"
        self.assertEqual(expected_value, result_value, msg=msg)

    def runArticleAssertions(self, article, fields):
        """ """
        for field in fields:
            expected_value = self.data["expected"][field]
            result_value = getattr(article, field, None)

            # handle checking datetimes...
            if field in ["publish_datetime_utc"]:
                self.assertEqual(type(result_value), type(datetime.today()))
                result_value = result_value.isoformat(sep=" ")

            # custom assertion for a given field
            assertion = "assert_%s" % field
            if hasattr(self, assertion):
                getattr(self, assertion)(field, expected_value, result_value)
                continue

            # default assertion
            msg = f"Error {field} \nexpected: {expected_value}\nresult:   {result_value}"
            self.assertEqual(expected_value, result_value, msg=msg)

    # def extract(self, instance):
    #     article_url = self.data['url']
    #     with requests_mock.mock() as m:
    #         for url, content in self.callback(self).contents():
    #             m.get(url, content=content)
    #         article = instance.extract(url=article_url)
    #         return article

    def getConfig(self):
        config = Configuration()
        config.enable_image_fetching = False
        return config

    def getArticle(self, config_=None):
        """ """
        # load test case data
        self.loadData()
        self.loadHtml()

        # basic configuration
        # no image fetching
        config = self.getConfig()
        if config is not None:
            if isinstance(config_, dict):
                for k, v in list(config_.items()):
                    if hasattr(config, k):
                        setattr(config, k, v)
        self.parser = config.get_parser()

        # target language
        # needed for non english language most of the time
        target_language = self.data.get("target_language")
        if target_language:
            config.target_language = target_language
            config.use_meta_language = False

        # read in the basic image...
        with open(f"{CURRENT_PATH}/data/images/50850547cc7310bc53e30e802c6318f1", "rb") as fobj:
            img_content = fobj.read()

        # read in another, blank image
        with open(f"{CURRENT_PATH}/data/images/blank.jpeg", "rb") as fobj:
            blank_img = fobj.read()

        # run goose
        with Goose(config=config) as g, requests_mock.Mocker(real_http=False) as m:
            # load images for those tests
            m.get("http://go.com/images/465395/", content=blank_img)
            m.get("http://bla.com/images/465395/", content=blank_img)
            m.get(
                "http://md0.libe.com/photo/465395/?modified_at=1351411813&ratio_x=03&ratio_y=02&width=476",
                content=img_content,
            )
            # if the url is not given in the result json, use the raw_html parameter.
            if "url" in self.data:
                m.get(self.data["url"], text=self.html)
                return g.extract(url=self.data["url"])
            else:
                return g.extract(raw_html=self.html)
