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


class PublishDateExtractor(BaseExtractor):
    def extract(self):
        # check the opengraph and ReportageNewsArticle dictionary for the
        # publication date first.
        if "article:published_time" in self.article.opengraph:
            return self.article.opengraph["article:published_time"]
        if self.article.schema and "datePublished" in self.article.schema:
            return self.article.schema["datePublished"]
        for known_meta_tag in self.config.known_publish_date_tags:
            # if this is a domain specific config and the current
            # article domain does not match the configured domain,
            # do not use the configured publish date pattern
            if known_meta_tag.domain and known_meta_tag.domain != self.article.domain:
                continue
            meta_tags = self.parser.getElementsByTag(self.article.doc,
                                                     attr=known_meta_tag.attr,
                                                     value=known_meta_tag.value,
                                                     tag=known_meta_tag.tag)
            if meta_tags:
                if known_meta_tag.tag is None:
                    content = self.parser.getAttribute(meta_tags[0], known_meta_tag.content)
                    # if not content try to get from other publish date tags
                    if not content:
                        continue
                    if known_meta_tag.subcontent:
                        try:
                            subcontent = json.loads(content)

                            return subcontent[known_meta_tag.subcontent]
                        except (ValueError, KeyError):
                            return None
                    return content
                else:
                    return meta_tags[0].text_content().strip()
        return None
