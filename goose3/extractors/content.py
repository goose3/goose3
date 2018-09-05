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
from copy import deepcopy

from goose3.extractors import BaseExtractor


class ContentExtractor(BaseExtractor):

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

    def get_known_article_tags(self):
        nodes = []
        for item in self.config.known_context_patterns:
            # if this is a domain specific config and the current
            # article domain does not match the configured domain,
            # do not use the configured content pattern
            if item.domain and self.article.domain != item.domain:
                continue

            nodes.extend(self.parser.getElementsByTag(self.article.doc, tag=item.tag,
                                                      attr=item.attr, value=item.value))
        if nodes:
            return nodes
        return None

    def is_articlebody(self, node):
        for item in self.config.known_context_patterns:
            # if this is a domain specific config and the current
            # article domain does not match the configured domain,
            # do not use the configured content pattern
            if item.domain and self.article.domain != item.domain:
                continue

            # attribute
            if item.attr:
                if self.parser.getAttribute(node, item.attr) == item.value:
                    return True

            # tag
            if item.tag:
                if node.tag == item.tag:
                    return True

        return False

    def calculate_best_node(self, doc):
        top_node = None
        nodes_to_check = self.nodes_to_check(doc)

        starting_boost = float(1.0)
        cnt = 0
        i = 0
        parent_nodes = []
        nodes_with_text = []

        for node in nodes_to_check:
            text_node = self.parser.getText(node)
            word_stats = self.stopwords_class(language=self.get_language()).get_stopword_count(text_node)
            high_link_density = self.is_highlink_density(node)
            if word_stats.get_stopword_count() > 2 and not high_link_density:
                nodes_with_text.append(node)

        nodes_number = len(nodes_with_text)
        negative_scoring = 0
        bottom_negativescore_nodes = float(nodes_number) * 0.25

        for node in nodes_with_text:
            boost_score = float(0)
            # boost
            if self.is_boostable(node):
                if cnt >= 0:
                    boost_score = float((1.0 / starting_boost) * 50)
                    starting_boost += 1
            # nodes_number
            if nodes_number > 15:
                if (nodes_number - i) <= bottom_negativescore_nodes:
                    booster = float(bottom_negativescore_nodes - (nodes_number - i))
                    boost_score = float(-pow(booster, float(2)))
                    negscore = abs(boost_score) + negative_scoring
                    if negscore > 40:
                        boost_score = float(5)

            text_node = self.parser.getText(node)
            word_stats = self.stopwords_class(language=self.get_language()).get_stopword_count(text_node)
            upscore = int(word_stats.get_stopword_count() + boost_score)

            # parent node
            parent_node = self.parser.getParent(node)
            self.update_score(parent_node, upscore)
            self.update_node_count(parent_node, 1)

            if parent_node not in parent_nodes:
                parent_nodes.append(parent_node)

            # parentparent node
            parent_parent_node = self.parser.getParent(parent_node)
            if parent_parent_node is not None:
                self.update_node_count(parent_parent_node, 1)
                self.update_score(parent_parent_node, upscore / 2)
                if parent_parent_node not in parent_nodes:
                    parent_nodes.append(parent_parent_node)
            cnt += 1
            i += 1

        top_node_score = 0
        for itm in parent_nodes:
            score = self.get_score(itm)

            if score > top_node_score:
                top_node = itm
                top_node_score = score

            if top_node is None:
                top_node = itm

        return top_node

    def is_boostable(self, node):
        """\
        alot of times the first paragraph might be the caption under an image
        so we'll want to make sure if we're going to boost a parent node that
        it should be connected to other paragraphs,
        at least for the first n paragraphs so we'll want to make sure that
        the next sibling is a paragraph and has at
        least some substatial weight to it
        """
        para = "p"
        steps_away = 0
        minimum_stopword_count = 5
        max_stepsaway_from_node = 3

        nodes = self.walk_siblings(node)
        for current_node in nodes:
            # p
            current_node_tag = self.parser.getTag(current_node)
            if current_node_tag == para:
                if steps_away >= max_stepsaway_from_node:
                    return False
                para_text = self.parser.getText(current_node)
                word_stats = self.stopwords_class(language=self.get_language()).get_stopword_count(para_text)
                if word_stats.get_stopword_count() > minimum_stopword_count:
                    return True
                steps_away += 1
        return False

    def walk_siblings(self, node):
        current_sibling = self.parser.previousSibling(node)
        res = []
        while current_sibling is not None:
            res.append(current_sibling)
            previous_sibling = self.parser.previousSibling(current_sibling)
            current_sibling = None if previous_sibling is None else previous_sibling
        return res

    def add_siblings(self, top_node):
        # in case the extraction used known attributes
        # we don't want to add sibilings
        if self.is_articlebody(top_node):
            return top_node
        baselinescore_siblings_para = self.get_siblings_score(top_node)
        results = self.walk_siblings(top_node)
        for current_node in results:
            prev_sibs = self.get_siblings_content(current_node, baselinescore_siblings_para)
            for prev in prev_sibs:
                top_node.insert(0, prev)
        return top_node

    def get_siblings_content(self, current_sibling, baselinescore_siblings_para):
        """
        adds any siblings that may have a decent score to this node
        """
        if current_sibling.tag == 'p' and self.parser.getText(current_sibling):
            tmp = current_sibling
            if tmp.tail:
                tmp = deepcopy(tmp)
                tmp.tail = ''
            return [tmp]
        else:
            potential_paragraphs = self.parser.getElementsByTag(current_sibling, tag='p')
            if potential_paragraphs is None:
                return None

            paragraphs = list()
            for first_paragraph in potential_paragraphs:
                text = self.parser.getText(first_paragraph)
                if text:  # no len(text) > 0
                    word_stats = self.stopwords_class(language=self.get_language()).get_stopword_count(text)
                    paragraph_score = word_stats.get_stopword_count()
                    sibling_baseline_score = float(.30)
                    high_link_density = self.is_highlink_density(first_paragraph)
                    score = float(baselinescore_siblings_para * sibling_baseline_score)
                    if score < paragraph_score and not high_link_density:
                        para = self.parser.createElement(tag='p', text=text, tail=None)
                        paragraphs.append(para)
            return paragraphs

    def get_siblings_score(self, top_node):
        """
        we could have long articles that have tons of paragraphs
        so if we tried to calculate the base score against
        the total text score of those paragraphs it would be unfair.
        So we need to normalize the score based on the average scoring
        of the paragraphs within the top node.
        For example if our total score of 10 paragraphs was 1000
        but each had an average value of 100 then 100 should be our base.
        """
        base = 100000
        paragraphs_number = 0
        paragraphs_score = 0
        nodes_to_check = self.parser.getElementsByTag(top_node, tag='p')

        for node in nodes_to_check:
            text_node = self.parser.getText(node)
            word_stats = self.stopwords_class(language=self.get_language()).get_stopword_count(text_node)
            high_link_density = self.is_highlink_density(node)
            if word_stats.get_stopword_count() > 2 and not high_link_density:
                paragraphs_number += 1
                paragraphs_score += word_stats.get_stopword_count()

        if paragraphs_number > 0:
            base = paragraphs_score // paragraphs_number

        return base

    def update_score(self, node, add_to_score):
        """
        adds a score to the gravityScore Attribute we put on divs
        we'll get the current score then add the score
        we're passing in to the current
        """
        current_score = 0
        score_string = self.parser.getAttribute(node, 'gravityScore')
        if score_string:
            current_score = int(score_string)

        new_score = current_score + int(add_to_score)
        self.parser.setAttribute(node, "gravityScore", str(new_score))

    def update_node_count(self, node, add_to_count):
        """\
        stores how many decent nodes are under a parent node
        """
        current_score = 0
        count_string = self.parser.getAttribute(node, 'gravityNodes')
        if count_string:
            current_score = int(count_string)

        new_score = current_score + add_to_count
        self.parser.setAttribute(node, "gravityNodes", str(new_score))

    def is_highlink_density(self, element):
        """
        checks the density of links within a node,
        is there not much text and most of it contains linky shit?
        if so it's no good
        """
        links = self.parser.getElementsByTag(element, tag='a')
        if not links:
            return False

        text = self.parser.getText(element)
        words = text.split(' ')
        words_number = float(len(words))
        link_text_parts = []
        for link in links:
            link_text_parts.append(self.parser.getText(link))

        link_text = ''.join(link_text_parts)
        link_words = link_text.split(' ')
        number_of_link_words = float(len(link_words))
        number_of_links = float(len(links))
        link_divisor = float(number_of_link_words / words_number)
        score = float(link_divisor * number_of_links)
        if score >= 1.0:
            return True
        return False
        # return True if score > 1.0 else False

    def get_score(self, node):
        """
        returns the gravityScore as an integer from this node
        """
        return self.get_node_gravity_score(node) or 0

    def get_node_gravity_score(self, node):
        grv_score_string = self.parser.getAttribute(node, 'gravityScore')
        if not grv_score_string:
            return None
        return int(grv_score_string)

    def nodes_to_check(self, docs):
        """\
        returns a list of nodes we want to search
        on like paragraphs and tables
        """
        nodes_to_check = []

        for doc in docs:
            for tag in ['p', 'pre', 'td']:
                items = self.parser.getElementsByTag(doc, tag=tag)
                nodes_to_check += items
        return nodes_to_check

    def is_table_and_no_para_exist(self, elm):
        sub_paragraphs = self.parser.getElementsByTag(elm, tag='p')
        for para in sub_paragraphs:
            txt = self.parser.getText(para)
            if len(txt) < 25:
                self.parser.remove(para)

        sub_paragraphs2 = self.parser.getElementsByTag(elm, tag='p')
        if not sub_paragraphs2 and elm.tag != "td":
            return True
        return False

    def is_nodescore_threshold_met(self, node, elm):
        top_node_score = self.get_score(node)
        current_node_score = self.get_score(elm)
        threshold_score = float(top_node_score * .08)

        if (current_node_score < threshold_score) and elm.tag != 'td':
            return False
        return True

    def post_cleanup(self):
        """\
        remove any divs that looks like non-content,
        clusters of links, or paras with no gusto
        """
        parse_tags = ['p']
        if self.config.parse_lists:
            parse_tags.extend(['ul', 'ol'])
        if self.config.parse_headers:
            parse_tags.extend(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

        target_node = self.article.top_node
        node = self.add_siblings(target_node)
        for elm in self.parser.getChildren(node):
            e_tag = self.parser.getTag(elm)
            if e_tag not in parse_tags:
                if (self.is_highlink_density(elm) or self.is_table_and_no_para_exist(elm) or
                        not self.is_nodescore_threshold_met(node, elm)):
                    self.parser.remove(elm)
        return node


class StandardContentExtractor(ContentExtractor):
    pass
