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
from goose3.extractors import BaseExtractor


class TweetsExtractor(BaseExtractor):
    def extract(self):
        tweets = []
        items = self.parser.get_elements_by_tag(
            self.article.top_node, tag="blockquote", attr="class", value="twitter-tweet"
        )

        for i in items:
            for attr in ["gravityScore", "gravityNodes"]:
                self.parser.del_attribute(i, attr)
            tweets.append(self.parser.node_to_string(i))

        return tweets
