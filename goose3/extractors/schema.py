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
        linked_data_nodes = self.parse_linked_data_nodes(metas)
        for linked_data in linked_data_nodes:
            try:
                if isinstance(linked_data, list):
                    for context in linked_data:
                        if context["@type"] in KNOWN_SCHEMA_TYPES:
                            return context
                elif isinstance(linked_data, dict):
                    if linked_data["@type"] in KNOWN_SCHEMA_TYPES:
                        return linked_data
            except (ValueError, KeyError):
                # If the contents are not proper JSON or a key we expect
                # to exist does not, continue to the next tag.
                continue
        return None

    def parse_linked_data_nodes(self, metas):
        linked_data = []
        for meta in metas:
            content = json.loads(meta.text_content())
            if content["@context"] in ("https://schema.org", "http://schema.org"):
                if content["@graph"]:
                    linked_data.extend(content["@graph"])
                else:
                    linked_data.extend(content)
        return linked_data
