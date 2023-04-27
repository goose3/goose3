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


class OpenGraphExtractor(BaseExtractor):
    def extract(self):
        opengraph_dict = {}
        node = self.article.doc
        metas = self.parser.get_elements_by_tag(node, "meta")

        # Open Graph type that is supported. In theory it is possible
        # that a page has multiple types
        og_types = [
            self.parser.get_attribute(meta, "content")
            for meta in metas
            if (self.parser.get_attribute(meta, "property") == "og:type" and self.parser.get_attribute(meta, "content"))
        ]

        if og_types:
            # make unique set of possible prefixes
            og_types = tuple(set(og_types))

        for meta in metas:
            attr = self.parser.get_attribute(meta, "property")
            value = self.parser.get_attribute(meta, "content")
            if attr and value:
                if attr.startswith("og:"):
                    self.__update_graph_dict(opengraph_dict, attr.split(":", 1)[1], value)
                elif og_types and attr.startswith(og_types):
                    self.__update_graph_dict(opengraph_dict, attr, value)

        # add all the types in... if there are multiple
        if len(og_types) > 1:
            opengraph_dict.pop("type")
            opengraph_dict["types"] = sorted(og_types)
        elif len(og_types) == 1:
            opengraph_dict["type"] = og_types[0]

        return opengraph_dict

    @staticmethod
    def __update_graph_dict(graph, key, val):
        if key not in graph:
            graph.update({key: val})
        elif not isinstance(graph.get(key), list):
            graph.update({key: [graph.get(key), val]})
        else:
            graph.update({key: graph.get(key) + [val]})
