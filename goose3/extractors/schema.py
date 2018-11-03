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

from goose3.extractors import BaseExtractor

KNOWN_SCHEMA_TYPES = (
    "ReportageNewsArticle",
    "NewsArticle",
    "Article"
)


class SchemaExtractor(BaseExtractor):

    def extract(self):
        node = self.article.doc
        metas = self.parser.getElementsByTag(node, 'script', attr='type',
                                             value='application/ld\\+json')
        for meta in metas:
            try:
                content = json.loads(meta.text_content())
                if isinstance(content, list):
                    for context in content:
                        if (context["@context"] == "http://schema.org" and
                                context["@type"] in KNOWN_SCHEMA_TYPES):
                            return content
                elif isinstance(content, dict):
                    if (content["@context"] == "http://schema.org" and
                            content["@type"] in KNOWN_SCHEMA_TYPES):
                        return content
            except (ValueError, KeyError):
                # If the contents are not proper JSON or a key we expect
                # to exist does not, continue to the next tag.
                continue
        return None
