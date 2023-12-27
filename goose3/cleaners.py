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
from goose3.utils import ReplaceSequence


class DocumentCleaner:
    def __init__(self, config, article):
        # config
        self.config = config

        # parser
        self.parser = self.config.get_parser()

        # article
        self.article = article

        # nodes to remove regexp
        self.remove_nodes_re = (
            "^side$|combx|retweet|mediaarticlerelated|menucontainer|"
            "navbar|storytopbar-bucket|utility-bar|inline-share-tools"
            "|comment|PopularQuestions|contact|foot|footer|Footer|footnote"
            "|cnn_strycaptiontxt|cnn_html_slideshow|cnn_strylftcntnt"
            "|^links$|meta$|shoutbox|sponsor"
            "|tags|socialnetworking|socialNetworking|cnnStryHghLght"
            "|cnn_stryspcvbx|^inset$|pagetools|post-attributes"
            "|welcome_form|contentTools2|the_answers"
            "|communitypromo|runaroundLeft|subscribe|vcard|articleheadings"
            "|date|^print$|popup|author-dropdown|tools|socialtools|byline"
            "|konafilter|KonaFilter|breadcrumbs|^fn$|wp-caption-text"
            "|legende|ajoutVideo|timestamp|js_replies|disclaim"
        )
        self.regexp_namespace = "http://exslt.org/regular-expressions"
        self.nauthy_ids_re = f"//*[re:test(@id, '{self.remove_nodes_re}', 'i')]"
        self.nauthy_classes_re = f"//*[re:test(@class, '{self.remove_nodes_re}', 'i')]"
        self.nauthy_names_re = f"//*[re:test(@name, '{self.remove_nodes_re}', 'i')]"
        # self.div_to_p_re = r"<(a|blockquote|dl|div|img|ol|p|pre|table|ul)"
        self.caption_re = "^caption$"
        self.google_re = " google "
        self.entries_re = "^[^entry-]more.*$"
        self.facebook_re = "[^-]facebook"
        self.facebook_braodcasting_re = "facebook-broadcasting"
        self.twitter_re = "[^-]twitter"
        self.tablines_replacements = ReplaceSequence().create("\n", "\n\n").append("\t").append("^\\s+$")

    def clean(self, doc_to_clean):
        doc_to_clean = self.clean_body_classes(doc_to_clean)
        doc_to_clean = self.clean_article_tags(doc_to_clean)
        doc_to_clean = self.clean_tags(doc_to_clean, ["em", "small"])
        doc_to_clean = self.remove_drop_caps(doc_to_clean)
        doc_to_clean = self.remove_scripts_styles(doc_to_clean)
        doc_to_clean = self.clean_bad_tags(doc_to_clean)
        doc_to_clean = self.remove_nodes_regex(doc_to_clean, self.caption_re)
        doc_to_clean = self.remove_nodes_regex(doc_to_clean, self.google_re)
        doc_to_clean = self.remove_nodes_regex(doc_to_clean, self.entries_re)
        doc_to_clean = self.remove_nodes_regex(doc_to_clean, self.facebook_re)
        doc_to_clean = self.remove_nodes_regex(doc_to_clean, self.facebook_braodcasting_re)
        doc_to_clean = self.remove_nodes_regex(doc_to_clean, self.twitter_re)
        doc_to_clean = self.clean_para_spans(doc_to_clean)
        doc_to_clean = self.div_to_para(doc_to_clean, "div")
        doc_to_clean = self.div_to_para(doc_to_clean, "span")
        return doc_to_clean

    def clean_body_classes(self, doc):
        # we don't need body classes
        # in case it matches an unwanted class all the document
        # will be empty
        elements = self.parser.get_elements_by_tag(doc, tag="body")
        if elements:
            self.parser.del_attribute(elements[0], attr="class")
        return doc

    def clean_article_tags(self, doc):
        articles = self.parser.get_elements_by_tag(doc, tag="article")
        for article in articles:
            for attr in ["id", "name", "class"]:
                self.parser.del_attribute(article, attr=attr)
        return doc

    def clean_tags(self, doc, tags):
        for tag in tags:
            itms = self.parser.get_elements_by_tag(doc, tag=tag)
            for node in itms:
                images = self.parser.get_elements_by_tag(node, tag="img")
                if len(images) == 0:
                    self.parser.drop_tag(node)
        return doc

    def remove_drop_caps(self, doc):
        items = self.parser.css_select(doc, "span[class~=dropcap], span[class~=drop_cap]")
        for item in items:
            self.parser.drop_tag(item)

        return doc

    def remove_scripts_styles(self, doc):
        # remove scripts
        scripts = self.parser.get_elements_by_tag(doc, tag="script")
        for item in scripts:
            self.parser.remove(item)

        # remove styles
        styles = self.parser.get_elements_by_tag(doc, tag="style")
        for item in styles:
            self.parser.remove(item)

        # remove comments
        comments = self.parser.get_comments(doc)
        for item in comments:
            self.parser.remove(item)

        return doc

    def clean_bad_tags(self, doc):
        # ids
        naughty_list = self.parser.xpath_re(doc, self.nauthy_ids_re)
        for node in naughty_list:
            self.parser.remove(node)

        # class
        naughty_classes = self.parser.xpath_re(doc, self.nauthy_classes_re)
        for node in naughty_classes:
            self.parser.remove(node)

        # name
        naughty_names = self.parser.xpath_re(doc, self.nauthy_names_re)
        for node in naughty_names:
            self.parser.remove(node)

        return doc

    def remove_nodes_regex(self, doc, pattern):
        for selector in ["id", "class"]:
            reg = f"//*[re:test(@{selector}, '{pattern}', 'i')]"
            naughty_list = self.parser.xpath_re(doc, reg)
            for node in naughty_list:
                self.parser.remove(node)
        return doc

    def clean_para_spans(self, doc):
        spans = self.parser.css_select(doc, "p span")
        for item in spans:
            self.parser.drop_tag(item)
        return doc

    def get_flushed_buffer(self, replacement_text):
        return self.parser.text_to_para(replacement_text)

    def get_replacement_nodes(self, div):
        replacement_text = []
        nodes_to_return = []
        nodes_to_remove = []
        childs = self.parser.child_nodes_with_text(div)

        for kid in childs:
            # node is a p
            # and already have some replacement text
            if self.parser.get_tag(kid) == "p" and len(replacement_text) > 0:
                new_node = self.get_flushed_buffer("".join(replacement_text))
                nodes_to_return.append(new_node)
                replacement_text = []
                nodes_to_return.append(kid)
            # node is a text node
            elif self.parser.is_text_node(kid):
                kid_text_node = kid
                kid_text = self.parser.get_text(kid)
                replace_text = self.tablines_replacements.replace_all(kid_text)
                if (len(replace_text)) > 1:
                    previous_sibling_node = self.parser.previous_sibling(kid_text_node)
                    while (
                        previous_sibling_node is not None
                        and self.parser.get_tag(previous_sibling_node) == "a"
                        and self.parser.get_attribute(previous_sibling_node, "grv-usedalready") != "yes"
                    ):
                        outer = " " + self.parser.outer_html(previous_sibling_node) + " "
                        replacement_text.append(outer)
                        nodes_to_remove.append(previous_sibling_node)
                        self.parser.set_attribute(previous_sibling_node, attr="grv-usedalready", value="yes")
                        prev = self.parser.previous_sibling(previous_sibling_node)
                        previous_sibling_node = prev if prev is not None else None
                    # append replace_text
                    replacement_text.append(replace_text)
                    #
                    next_sibling_node = self.parser.next_sibling(kid_text_node)
                    while (
                        next_sibling_node is not None
                        and self.parser.get_tag(next_sibling_node) == "a"
                        and self.parser.get_attribute(next_sibling_node, "grv-usedalready") != "yes"
                    ):
                        outer = " " + self.parser.outer_html(next_sibling_node) + " "
                        replacement_text.append(outer)
                        nodes_to_remove.append(next_sibling_node)
                        self.parser.set_attribute(next_sibling_node, attr="grv-usedalready", value="yes")
                        next_sib = self.parser.next_sibling(next_sibling_node)
                        previous_sibling_node = next_sib if next_sib is not None else None

            # otherwise
            else:
                nodes_to_return.append(kid)

        # flush out anything still remaining
        if len(replacement_text) > 0:
            new_node = self.get_flushed_buffer("".join(replacement_text))
            nodes_to_return.append(new_node)
            replacement_text = []

        for node in nodes_to_remove:
            self.parser.remove(node)

        return nodes_to_return

    def replace_with_para(self, div):
        self.parser.replace_tag(div, "p")

    def div_to_para(self, doc, dom_type):
        bad_divs = 0
        else_divs = 0
        divs = self.parser.get_elements_by_tag(doc, tag=dom_type)
        tags = ["a", "blockquote", "dl", "div", "img", "ol", "p", "pre", "table", "ul"]

        for div in divs:
            items = self.parser.get_elements_by_tags(div, tags)
            if div is not None and len(items) == 0:
                self.replace_with_para(div)
                bad_divs += 1
            elif div is not None:
                replace_nodes = self.get_replacement_nodes(div)
                for child in self.parser.child_nodes(div):
                    div.remove(child)

                for i, node in enumerate(replace_nodes):
                    div.insert(i, node)

                else_divs += 1

        return doc


class StandardDocumentCleaner(DocumentCleaner):
    pass
