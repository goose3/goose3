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

from goose3.extractors import BaseExtractor


class AuthorsExtractor(BaseExtractor):

    def extract(self):
        authors = set()

        for known_tag in self.config.known_author_patterns:
            meta_tags = self.parser.getElementsByTag(self.article.doc,
                                                     attr=known_tag.attr,
                                                     value=known_tag.value,
                                                     tag=known_tag.tag)
            if not meta_tags:
                continue

            for meta_tag in meta_tags:

                if known_tag.subpattern:
                    name_nodes = self.parser.getElementsByTag(meta_tag,
                                                              attr=known_tag.subpattern.attr,
                                                              value=known_tag.subpattern.value,
                                                              tag=known_tag.subpattern.tag)

                    if len(name_nodes) > 0:
                        name = self.parser.getText(name_nodes[0])
                        authors.add(name)
                else:
                    if known_tag.tag is None:
                        name = self.parser.getAttribute(meta_tag, known_tag.content)
                        if not name:
                            continue

                        authors.add(name)
                    else:
                        authors.add(meta_tag.text_content().strip())
        return list(authors)
