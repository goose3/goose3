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
from .test_base import TestExtractionBase


class TestArticleAuthor(TestExtractionBase):
    def test_author_schema(self):
        field = "authors"

        # Do not call self.runArticleAssertions because need to sort results,
        # because set not save ordering, so test failed;
        article = self.getArticle()

        expected_value = self.data["expected"][field]
        result_value = getattr(article, field, None)

        expected_value.sort()
        result_value.sort()

        # default assertion
        msg = f"Error {field} \nexpected: {expected_value}\nresult: {result_value}"
        self.assertEqual(expected_value, result_value, msg=msg)

    def test_author_config(self):
        field = "authors"

        # Do not call self.runArticleAssertions because need to sort results,
        # because set not save ordering, so test failed;

        config = {
            "known_author_patterns": [
                {"tag": "span", "attribute": "class", "value": "author", "content": "content"},
                {
                    "tag": "span",
                    "attribute": "class",
                    "value": "byline",
                    "subpattern": {"attribute": "itemprop", "value": "name", "content": "data-byline-name"},
                },
            ]
        }
        article = self.getArticle(config_=config)
        expected_value = self.data["expected"][field]
        result_value = getattr(article, field, None)

        expected_value.sort()
        result_value.sort()

        # default assertion
        msg = f"Error {field} \nexpected: {expected_value}\nresult: {result_value}"
        self.assertEqual(expected_value, result_value, msg=msg)

    def test_author_linked_data(self):
        field = "authors"

        article = self.getArticle()

        expected_value = self.data["expected"][field]
        result_value = getattr(article, field, None)

        expected_value.sort()
        result_value.sort()

        msg = f"Error {field} \nexpected: {expected_value}\nresult: {result_value}"
        self.assertEqual(expected_value, result_value, msg=msg)
