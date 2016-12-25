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
import json
import os
import unittest

import requests_mock

try:
    import urllib2
except ImportError:
    import urllib.request as urllib2

from goose import Goose
from goose.utils import FileHelper
from goose.configuration import Configuration

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


class TestExtractionBase(unittest.TestCase):
    """\
    Extraction test case
    """
    # callback = MockResponseExtractors

    def getRawHtml(self):
        test, suite, module, cls, func = self.id().split('.')
        path = os.path.join(
            os.path.dirname(CURRENT_PATH),
            "data",
            suite,
            module.partition('test_')[2],
            "%s.html" % func)
        path = os.path.abspath(path)
        content = FileHelper.loadResourceFile(path)
        return content

    def loadData(self):
        """\

        """
        full_id = self.id().split('.')

        test, module, cls, func = full_id
        path = os.path.join(
            os.path.dirname(CURRENT_PATH),
            'tests',
            "data",
            # suite,
            module.partition('test_')[2],
            "%s.json" % func)
        path = os.path.abspath(path)
        content = FileHelper.loadResourceFile(path)
        self.data = json.loads(content)

    def loadHtml(self):
        test, module, cls, func = self.id().split('.')
        path = os.path.join(
            os.path.dirname(CURRENT_PATH),
            'tests',
            "data",
            module.partition('test_')[2],
            "%s.html" % func)
        path = os.path.abspath(path)
        self.html = FileHelper.loadResourceFile(path)

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
        result_value = result_value[0:len(expected_value)]
        msg = "The beginning of the article text was not as expected!"
        self.assertEqual(expected_value, result_value, msg=msg)

    def runArticleAssertions(self, article, fields):
        """\

        """
        for field in fields:
            expected_value = self.data['expected'][field]
            result_value = getattr(article, field, None)

            # custom assertion for a given field
            assertion = 'assert_%s' % field
            if hasattr(self, assertion):
                getattr(self, assertion)(field, expected_value, result_value)
                continue

            # default assertion
            msg = "Error %s \nexpected: %s\nresult: %s" % (field, expected_value, result_value)
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

    def getArticle(self):
        """\

        """
        # load test case data
        self.loadData()
        self.loadHtml()

        # basic configuration
        # no image fetching
        config = self.getConfig()
        self.parser = config.get_parser()

        # target language
        # needed for non english language most of the time
        target_language = self.data.get('target_language')
        if target_language:
            config.target_language = target_language
            config.use_meta_language = False

        with requests_mock.Mocker(real_http=True) as m:
            m.get(self.data['url'], text=self.html)
            # run goose
            g = Goose(config=config)
            return g.extract(url=self.data['url'])
