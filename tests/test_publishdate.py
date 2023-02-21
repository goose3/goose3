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
from goose3 import Configuration, PublishDatePattern

from .test_base import TestExtractionBase


class TestPublishDate(TestExtractionBase):
    def test_publish_date(self):
        article = self.getArticle()
        self.runArticleAssertions(article=article, fields=["publish_date", "publish_datetime_utc"])

    def test_publish_date_rnews(self):
        article = self.getArticle()
        self.runArticleAssertions(article=article, fields=["publish_date", "publish_datetime_utc"])

    def test_publish_date_article(self):
        article = self.getArticle()
        self.runArticleAssertions(article=article, fields=["publish_date", "publish_datetime_utc"])

    def test_publish_date_schema(self):
        article = self.getArticle()
        self.runArticleAssertions(article=article, fields=["publish_date", "publish_datetime_utc"])

    def test_publish_date_unix_milliseconds(self):
        article = self.getArticle()
        self.runArticleAssertions(article=article, fields=["publish_date", "publish_datetime_utc"])

    def test_publish_date_unix_seconds(self):
        article = self.getArticle()
        self.runArticleAssertions(article=article, fields=["publish_date", "publish_datetime_utc"])

    def test_publish_date_parsely_page(self):
        article = self.getArticle()
        self.runArticleAssertions(article=article, fields=["publish_date", "publish_datetime_utc"])

    def test_publish_date_tag(self):
        config = {"known_publish_date_tags": {"attribute": "class", "value": "pubdate", "tag": "div"}}
        article = self.getArticle(config)
        self.runArticleAssertions(article=article, fields=["publish_date", "publish_datetime_utc"])

    def test_publish_date_config(self):
        # Test with configuring the pubdate with a dict and no domain filter
        config0 = {"known_publish_date_tags": {"attribute": "name", "value": "super-rare-date-tag", "content": "value"}}
        article = self.getArticle(config_=config0)
        self.runArticleAssertions(article=article, fields=["publish_date", "publish_datetime_utc"])

        # Test with configuring the pubdate with a PublishDatePattern and no domain filter
        config1 = {
            "known_publish_date_tags": PublishDatePattern(attr="name", value="super-rare-date-tag", content="value")
        }
        article = self.getArticle(config_=config1)
        self.runArticleAssertions(article=article, fields=["publish_date", "publish_datetime_utc"])

        # Test with configuring the incorrect domain filter
        config2 = {
            "known_publish_date_tags": PublishDatePattern(
                attr="name", value="super-rare-date-tag", content="value", domain="incorrect.com"
            )
        }
        article = self.getArticle(config_=config2)
        assert not article.publish_date
        assert not article.publish_datetime_utc

        # Test with configuring the correct domain filter
        config3 = {
            "known_publish_date_tags": PublishDatePattern(
                attr="name", value="super-rare-date-tag", content="value", domain="example.com"
            )
        }
        article = self.getArticle(config_=config3)
        self.runArticleAssertions(article=article, fields=["publish_date", "publish_datetime_utc"])
