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
import json

from goose3.extractors import BaseExtractor

KNOWN_SCHEMA_TYPES = ("ReportageNewsArticle", "NewsArticle", "Article")


class SchemaExtractor(BaseExtractor):
    def extract(self):
        node = self.article.doc
        metas = self.parser.get_elements_by_tag(node, "script", attr="type", value="application/ld\\+json")
        linked_data_nodes = self.__parse_linked_data_nodes(metas)
        for linked_data in linked_data_nodes:
            if "@type" in linked_data and linked_data["@type"] in KNOWN_SCHEMA_TYPES:
                return linked_data
        return None

    def __parse_linked_data_nodes(self, metas):
        linked_data = []
        for meta in metas:
            try:
                content = json.loads(meta.text_content())
                if isinstance(content, list):
                    linked_data.extend([context for context in content if self.__validate_context(context)])
                elif isinstance(content, dict) and self.__validate_context(content):
                    if "@graph" in content:
                        linked_data.extend(content["@graph"])
                    else:
                        linked_data.append(content)
            except (ValueError, KeyError):
                # If the contents are not proper JSON or a key we expect
                # to exist does not, continue to the next tag.
                continue
        return linked_data

    def __validate_context(self, content):
        if "@context" in content:
            return content["@context"] in ("https://schema.org", "http://schema.org")
        return False
