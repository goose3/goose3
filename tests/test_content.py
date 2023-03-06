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
from goose3 import ArticleContextPattern
from goose3.text import StopWordsArabic, StopWordsChinese, StopWordsKorean

from .test_base import TestExtractionBase


class TestExtractions(TestExtractionBase):
    def test_allnewlyrics1(self):
        article = self.getArticle()
        fields = ["title", "cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_cnn1(self):
        article = self.getArticle()
        fields = ["title", "cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_businessWeek1(self):
        article = self.getArticle()
        fields = ["title", "cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_businessWeek2(self):
        article = self.getArticle()
        fields = ["title", "cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_businessWeek3(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_businessWeek4(self):
        article = self.getArticle({"parse_headers": False})
        fields = ["title", "cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_cbslocal(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_elmondo1(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_elpais(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_liberation(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_lefigaro(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_techcrunch1(self):
        article = self.getArticle()
        fields = ["title", "cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_foxNews(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_aolNews(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_huffingtonPost2(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_testHuffingtonPost(self):
        article = self.getArticle()
        fields = [
            "cleaned_text",
            "meta_description",
            "title",
        ]
        self.runArticleAssertions(article=article, fields=fields)

    def test_espn(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_engadget(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_msn1(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_guardian1(self):
        article = self.getArticle({"parse_headers": False, "parse_lists": False})
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_time(self):
        article = self.getArticle()
        fields = ["cleaned_text", "title"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_time2(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_cnet(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_yahoo(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_politico(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_businessinsider3(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_cnbc1(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_marketplace(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_issue24(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_issue25(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_issue28(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_issue32(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_issue4(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_gizmodo1(self):
        article = self.getArticle()
        fields = ["cleaned_text", "meta_description", "meta_keywords"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_gizmodo2(self):
        article = self.getArticle(config_={"enable_image_fetching": False, "pretty_lists": False})
        fields = ["cleaned_text", "meta_description", "meta_keywords"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_gizmodo3(self):
        article = self.getArticle({"parse_lists": False})
        fields = ["cleaned_text", "meta_description", "meta_keywords"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_mashable_issue_74(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_usatoday_issue_74(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_okaymarketing(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_issue129(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_issue115(self):
        # https://github.com/grangier/python-goose/issues/115
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_pattern_config(self):
        fields = ["cleaned_text"]
        # Test with configuring the content pattern with a dict and no domain filter
        config0 = {"known_context_patterns": {"attr": "class", "value": "super-rare-article-tag"}}
        article = self.getArticle(config_=config0)
        self.runArticleAssertions(article=article, fields=fields)

        # Test with configuring the pubdate with a PublishDatePattern and no domain filter
        config1 = {"known_context_patterns": ArticleContextPattern(attr="class", value="super-rare-article-tag")}
        article = self.getArticle(config_=config1)
        self.runArticleAssertions(article=article, fields=fields)

        # Test with configuring the incorrect domain filter
        config2 = {
            "known_context_patterns": ArticleContextPattern(
                attr="class", value="super-rare-article-tag", domain="incorrect.com"
            )
        }
        article = self.getArticle(config_=config2)
        assert article.cleaned_text == "This should not be included."

        # Test with configuring the correct domain filter
        config3 = {
            "known_context_patterns": ArticleContextPattern(
                attr="class", value="super-rare-article-tag", domain="example.com"
            )
        }
        article = self.getArticle(config_=config3)
        self.runArticleAssertions(article=article, fields=fields)

    def test_retry_top_node(self):
        article = self.getArticle()
        self.runArticleAssertions(article=article, fields=["cleaned_text", "top_node_raw_html"])

    def test_wiwo(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)


class TestArticleTopNode(TestExtractionBase):
    def test_articlebody_itemprop(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_articlebody_attribute(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_articlebody_tag(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)


class TestExtractWithUrl(TestExtractionBase):
    def test_get_canonical_url(self):
        article = self.getArticle()
        fields = ["cleaned_text", "canonical_link"]
        self.runArticleAssertions(article=article, fields=fields)


class TestExtractChinese(TestExtractionBase):
    def getConfig(self):
        config = super().getConfig()
        config.stopwords_class = StopWordsChinese
        return config

    def test_bbc_chinese(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)


class TestExtractArabic(TestExtractionBase):
    def getConfig(self):
        config = super().getConfig()
        config.stopwords_class = StopWordsArabic
        return config

    def test_cnn_arabic(self):
        article = self.getArticle()
        fields = ["cleaned_text"]
        self.runArticleAssertions(article=article, fields=fields)


class TestExtractKorean(TestExtractionBase):
    def getConfig(self):
        config = super().getConfig()
        config.stopwords_class = StopWordsKorean
        return config

    def test_donga_korean(self):
        article = self.getArticle()
        fields = ["cleaned_text", "meta_description", "meta_keywords"]
        self.runArticleAssertions(article=article, fields=fields)


class TestExtractionsRaw(TestExtractions):
    def extract(self, instance):
        article = instance.extract(raw_html=self.getRawHtml())
        return article
