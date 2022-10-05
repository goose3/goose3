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
import html

from goose3.text import inner_trim


class OutputFormatter:
    def __init__(self, config, article):
        # config
        self.config = config

        # article
        self.article = article

        # parser
        self.parser = self.config.get_parser()

        # stopwords class
        self.stopwords_class = config.stopwords_class

        # top node
        self.top_node = None

    def get_language(self):
        """
        Returns the language is by the article or
        the configuration language
        """
        # we don't want to force the target language
        # so we use the article.meta_lang
        if self.config.use_meta_language:
            if self.article.meta_lang:
                return self.article.meta_lang[:2]
        return self.config.target_language

    def get_top_node(self):
        return self.top_node

    def get_formatted_text(self):
        self.top_node = self.article.top_node
        self.remove_negativescores_nodes()
        self.links_to_text()
        self.add_newline_to_br()
        self.replace_with_text()
        self.remove_fewwords_paragraphs()
        self.make_list_elms_pretty()
        return self.convert_to_text()

    def convert_to_text(self):
        txts = []
        for node in list(self.get_top_node()):
            txt = self.parser.get_text(node)
            if txt:
                txt = html.unescape(txt)
                txt_lis = inner_trim(txt).split(r"\n")
                txts.extend(txt_lis)
        text = "\n\n".join(txts)
        # ensure no double newlines at the beginning of lists
        if self.config.parse_lists:
            # Split out the lists and clean them up! Ensuring no trailing spaces
            txt = text.replace("\n•", "•").split("• ")
            txt = [x.strip() for x in txt]

            if self.config.pretty_lists:
                text = "\n• ".join(txt)
            else:
                text = "\n".join(txt)
        return text

    def add_newline_to_br(self):
        for elm in self.parser.get_elements_by_tag(self.top_node, tag="br"):
            elm.text = r"\n"

    def links_to_text(self):
        """cleans up and converts any nodes that should be considered text into text"""
        self.parser.strip_tags(self.get_top_node(), "a")

    def make_list_elms_pretty(self):
        """make any list element read like a list"""
        for elm in self.parser.get_elements_by_tag(self.top_node, tag="li"):
            elm.text = rf"• {elm.text}"

    def remove_negativescores_nodes(self):
        """if there are elements inside our top node that have a negative gravity score, let's give em the boot"""
        gravity_items = self.parser.css_select(self.top_node, "*[gravityScore]")
        for item in gravity_items:
            score = self.parser.get_attribute(item, "gravityScore")
            score = int(score, 0)
            if score < 1:
                item.getparent().remove(item)

    def replace_with_text(self):
        """replace common tags with just text so we don't have any crazy formatting issues
        so replace <br>, <i>, <strong>, etc.... with whatever text is inside them
        code : http://lxml.de/api/lxml.etree-module.html#strip_tags
        """
        self.parser.strip_tags(self.get_top_node(), "b", "strong", "i", "br")
        if self.config.keep_footnotes:
            self.parser.strip_tags(self.get_top_node(), "sup")

    def remove_fewwords_paragraphs(self):
        """remove paragraphs that have less than x number of words, would indicate that it's some sort of link"""
        all_nodes = self.parser.get_elements_by_tags(self.get_top_node(), ["*"])
        all_nodes.reverse()
        for elm in all_nodes:
            tag = self.parser.get_tag(elm)
            text = self.parser.get_text(elm)
            stop_words = self.stopwords_class(language=self.get_language()).get_stopword_count(text)
            if (
                (tag != "br" or text != "\\r")
                and stop_words.get_stopword_count() < 3
                and len(self.parser.get_elements_by_tag(elm, tag="object")) == 0
                and len(self.parser.get_elements_by_tag(elm, tag="embed")) == 0
            ):
                self.parser.remove(elm)
            # TODO
            # check if it is in the right place
            else:
                trimmed = self.parser.get_text(elm)
                if trimmed.startswith("(") and trimmed.endswith(")"):
                    self.parser.remove(elm)


class StandardOutputFormatter(OutputFormatter):
    pass
