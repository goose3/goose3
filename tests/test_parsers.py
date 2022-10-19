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
import codecs
import os
import unittest

from goose3.parsers import Parser, ParserSoup
from goose3.utils.constants import CAMEL_CASE_DEPRICATION
from tests.test_base import fail_after

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


def load_resource(path):
    try:
        with codecs.open(path, "r", "utf-8") as fobj:
            content = fobj.read()
        return content
    except OSError:
        raise OSError("Couldn't open file %s" % path)


class ParserBase(unittest.TestCase):
    def setUp(self):
        self.parser = Parser

    def get_html(self, filename):
        path = os.path.join(CURRENT_PATH, "data", filename)
        path = os.path.abspath(path)
        return load_resource(path)

    def test_cssselect(self):
        html = "<html><body>"
        html += '<p class="link">this is a test <a class="link">link</a> and this is <strong class="foo">strong</strong></p>'
        html += '<p>this is a test and this is <strong class="link">strong</strong></p>'
        html += "</body></html>"
        doc = self.parser.fromstring(html)
        # find node with a class attribute
        items_result = self.parser.css_select(doc, "*[class]")
        self.assertEqual(len(items_result), 4)

        # find p nodes
        items_result = self.parser.css_select(doc, "p")
        self.assertEqual(len(items_result), 2)

        # find nodes with attribute class equal to link
        items_result = self.parser.css_select(doc, "*[class=link]")
        self.assertEqual(len(items_result), 3)

        # find p nodes with class attribute
        items_result = self.parser.css_select(doc, "p[class]")
        self.assertEqual(len(items_result), 1)

        # find p nodes with class attribute link
        items_result = self.parser.css_select(doc, "p[class=link]")
        self.assertEqual(len(items_result), 1)

        # find strong nodes with class attribute link or foo
        items_result = self.parser.css_select(doc, "strong[class=link], strong[class=foo]")
        self.assertEqual(len(items_result), 2)

        # find strong nodes with class attribute link or foo
        items_result = self.parser.css_select(doc, "p > a")
        self.assertEqual(len(items_result), 1)

    def test_get_elements_by_tag(self):
        html = "<html><body>"
        html += '<p>this is a test <a class="link">link</a> and this is <strong class="link">strong</strong></p>'
        html += '<p>this is a test and this is <strong class="link">strong</strong></p>'
        html += "</body></html>"
        doc = self.parser.fromstring(html)
        p = self.parser.get_elements_by_tag(doc, tag="p")[0]

        self.assertEqual(len(p), 2)

    def test_replace_tag(self):
        html = self.get_html("parser/test1.html")
        doc = self.parser.fromstring(html)

        # replace all p with div
        ps = self.parser.get_elements_by_tag(doc, tag="p")
        divs = self.parser.get_elements_by_tag(doc, tag="div")
        pcount = len(ps)
        divcount = len(divs)
        for p in ps:
            self.parser.replace_tag(p, "div")
        divs2 = self.parser.get_elements_by_tag(doc, tag="div")
        divcount2 = len(divs2)
        self.assertEqual(divcount2, pcount + divcount)

        # replace first div span with center
        spans = self.parser.get_elements_by_tag(doc, tag="span")
        spanscount = len(spans)
        div = self.parser.get_elements_by_tag(doc, tag="div")[0]
        span = self.parser.get_elements_by_tag(div, tag="span")
        self.assertEqual(len(span), 1)
        self.parser.replace_tag(span[0], "center")
        span = self.parser.get_elements_by_tag(div, tag="span")
        self.assertEqual(len(span), 0)
        centers = self.parser.get_elements_by_tag(div, tag="center")
        self.assertEqual(len(centers), 1)

    def test_droptag(self):
        # test with 1 node
        html = "<html><body><div>Hello <b>World!</b></div></body></html>"
        expecte_html = "<html><body><div>Hello World!</div></body></html>"
        doc = self.parser.fromstring(html)
        nodes = self.parser.css_select(doc, "b")
        self.assertEqual(len(nodes), 1)
        self.parser.drop_tag(nodes)

        nodes = self.parser.css_select(doc, "b")
        self.assertEqual(len(nodes), 0)

        result_html = self.parser.node_to_string(doc)
        self.assertEqual(expecte_html, result_html)

        # test with 2 nodes
        html = "<html><body><div>Hello <b>World!</b> bla <b>World!</b></div></body></html>"
        expecte_html = "<html><body><div>Hello World! bla World!</div></body></html>"
        doc = self.parser.fromstring(html)
        nodes = self.parser.css_select(doc, "b")
        self.assertEqual(len(nodes), 2)
        self.parser.drop_tag(nodes)

        nodes = self.parser.css_select(doc, "b")
        self.assertEqual(len(nodes), 0)

        result_html = self.parser.node_to_string(doc)
        self.assertEqual(expecte_html, result_html)

    def test_tostring(self):
        html = "<html><body>"
        html += "<p>this is a test <a>link</a> and this is <strong>strong</strong></p>"
        html += "</body></html>"
        doc = self.parser.fromstring(html)
        result = self.parser.node_to_string(doc)
        self.assertEqual(html, result)

    def test_strip_tags(self):
        html = "<html><body>"
        html += "<p>this is a test <a>link</a> and this is <strong>strong</strong></p>"
        html += "</body></html>"
        expected = "<html><body>"
        expected += "<p>this is a test link and this is strong</p>"
        expected += "</body></html>"
        doc = self.parser.fromstring(html)
        self.parser.strip_tags(doc, "a", "strong")
        result = self.parser.node_to_string(doc)
        self.assertEqual(expected, result)

    def test_get_elements_by_tags(self):
        html = "<html><body>"
        html += '<p>this is a test <a class="link">link</a> and this is <strong class="link">strong</strong></p>'
        html += '<p>this is a test and this is <strong class="link">strong</strong></p>'
        html += "</body></html>"
        doc = self.parser.fromstring(html)
        elements = self.parser.get_elements_by_tags(doc, ["p", "a", "strong"])
        self.assertEqual(len(elements), 5)

        # find childs within the first p
        p = self.parser.get_elements_by_tag(doc, tag="p")[0]
        elements = self.parser.get_elements_by_tags(p, ["p", "a", "strong"])
        self.assertEqual(len(elements), 2)

    def test_get_elements_by_tag(self):
        html = "<html><body>"
        html += "<p>this is a test <a>link</a> and this is <strong>strong</strong></p>"
        html += "</body></html>"
        doc = self.parser.fromstring(html)
        # find all tags
        elements = self.parser.get_elements_by_tag(doc)
        self.assertEqual(len(elements), 5)

        # find all p
        elements = self.parser.get_elements_by_tag(doc, tag="p")
        self.assertEqual(len(elements), 1)

        html = "<html><body>"
        html += '<p>this is a test <a class="link classB classc">link</a> and this is <strong class="link">strong</strong></p>'
        html += '<p>this is a test and this is <strong class="Link">strong</strong></p>'
        html += "</body></html>"
        doc = self.parser.fromstring(html)
        # find all p
        elements = self.parser.get_elements_by_tag(doc, tag="p")
        self.assertEqual(len(elements), 2)

        # find all a
        elements = self.parser.get_elements_by_tag(doc, tag="a")
        self.assertEqual(len(elements), 1)

        # find all strong
        elements = self.parser.get_elements_by_tag(doc, tag="strong")
        self.assertEqual(len(elements), 2)

        # find first p
        # and find strong elemens within the p
        elem = self.parser.get_elements_by_tag(doc, tag="p")[0]
        elements = self.parser.get_elements_by_tag(elem, tag="strong")
        self.assertEqual(len(elements), 1)

        # test if the first p in taken in account
        elem = self.parser.get_elements_by_tag(doc, tag="p")[0]
        elements = self.parser.get_elements_by_tag(elem, tag="p")
        self.assertEqual(len(elements), 0)

        # find elem with class "link"
        elements = self.parser.get_elements_by_tag(doc, attr="class", value="link")
        self.assertEqual(len(elements), 3)

        # find elem with class "classB"
        elements = self.parser.get_elements_by_tag(doc, attr="class", value="classB")
        self.assertEqual(len(elements), 1)

        # find elem with class "classB"
        elements = self.parser.get_elements_by_tag(doc, attr="class", value="classc")
        self.assertEqual(len(elements), 1)

        # find elem with class "link" with tag strong
        elements = self.parser.get_elements_by_tag(doc, tag="strong", attr="class", value="link")
        self.assertEqual(len(elements), 2)

        # find elem with class "link" with tag strong
        # within the second p
        elem = self.parser.get_elements_by_tag(doc, tag="p")[1]
        elements = self.parser.get_elements_by_tag(elem, tag="strong", attr="class", value="link")
        self.assertEqual(len(elements), 1)

    def test_del_attribute(self):
        html = self.get_html("parser/test1.html")
        doc = self.parser.fromstring(html)

        # find div element with class foo
        elements = self.parser.get_elements_by_tag(doc, tag="div", attr="class", value="foo")
        self.assertEqual(len(elements), 1)

        div = elements[0]
        # remove an unexistant attribute
        self.parser.del_attribute(div, attr="bla")
        # remove the attribute class
        self.parser.del_attribute(div, attr="class")

        # find div element with class foo
        elements = self.parser.get_elements_by_tag(doc, tag="div", attr="class", value="foo")
        self.assertEqual(len(elements), 0)

    def test_encoding(self):
        """
        If pass unicode string to lxml.html.fromstring with encoding set in document will receive:
        "ValueError: Unicode strings with encoding declaration are not supported.
        Please use bytes input or XML fragments without declaration."
        Test for this case.
        """
        html = """
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        """
        html += "<html><body>"
        html += "<p>Я рядочок</p>"
        html += "</body></html>"
        self.parser.fromstring(html)

    @fail_after(CAMEL_CASE_DEPRICATION, "nodeToString")
    def test_tostring_old(self):
        html = "<html><body>"
        html += "<p>this is a test <a>link</a> and this is <strong>strong</strong></p>"
        html += "</body></html>"
        doc = self.parser.fromstring(html)
        result = self.parser.nodeToString(doc)
        self.assertEqual(html, result)

    @fail_after(CAMEL_CASE_DEPRICATION, "replaceTag")
    def test_replace_tag_old(self):
        html = self.get_html("parser/test1.html")
        doc = self.parser.fromstring(html)

        # replace all p with div
        ps = self.parser.get_elements_by_tag(doc, tag="p")
        divs = self.parser.get_elements_by_tag(doc, tag="div")
        pcount = len(ps)
        divcount = len(divs)
        for p in ps:
            self.parser.replaceTag(p, "div")
        divs2 = self.parser.get_elements_by_tag(doc, tag="div")
        divcount2 = len(divs2)
        self.assertEqual(divcount2, pcount + divcount)

    @fail_after(CAMEL_CASE_DEPRICATION, "stripTags")
    def test_strip_tags_old(self):
        html = "<html><body>"
        html += "<p>this is a test <a>link</a> and this is <strong>strong</strong></p>"
        html += "</body></html>"
        expected = "<html><body>"
        expected += "<p>this is a test link and this is strong</p>"
        expected += "</body></html>"
        doc = self.parser.fromstring(html)
        self.parser.stripTags(doc, "a", "strong")
        result = self.parser.node_to_string(doc)
        self.assertEqual(expected, result)

    @fail_after(CAMEL_CASE_DEPRICATION, "getElementById")
    def test_get_element_by_id_old(self):  # TODO: currently there isn't one that tests this functionality directly
        self.assertTrue(True)

    @fail_after(CAMEL_CASE_DEPRICATION, "getElementsByTag")
    def test_get_elements_by_tag_old(self):
        html = "<html><body>"
        html += '<p>this is a test <a class="link">link</a> and this is <strong class="link">strong</strong></p>'
        html += '<p>this is a test and this is <strong class="link">strong</strong></p>'
        html += "</body></html>"
        doc = self.parser.fromstring(html)
        p = self.parser.getElementsByTag(doc, tag="p")[0]

        self.assertEqual(len(p), 2)

    @fail_after(CAMEL_CASE_DEPRICATION, "appendChild")
    def test_append_child_old(self):  # TODO: currently there isn't one that tests this functionality directly
        self.assertTrue(True)

    @fail_after(CAMEL_CASE_DEPRICATION, "childNodes")
    def test_child_nodes_old(self):  # TODO: currently there isn't one that tests this functionality directly
        self.assertTrue(True)

    @fail_after(CAMEL_CASE_DEPRICATION, "childNodesWithText")
    def test_child_nodes_with_text_old(self):  # TODO: currently there isn't one that tests this functionality directly
        self.assertTrue(True)

    @fail_after(CAMEL_CASE_DEPRICATION, "textToPara")
    def test_text_to_para_old(self):  # TODO: currently there isn't one that tests this functionality directly
        self.assertTrue(True)

    @fail_after(CAMEL_CASE_DEPRICATION, "getChildren")
    def test_get_children_old(self):  # TODO: currently there isn't one that tests this functionality directly
        self.assertTrue(True)

    @fail_after(CAMEL_CASE_DEPRICATION, "getElementsByTags")
    def test_get_elements_by_tags_old(self):
        html = "<html><body>"
        html += '<p>this is a test <a class="link">link</a> and this is <strong class="link">strong</strong></p>'
        html += '<p>this is a test and this is <strong class="link">strong</strong></p>'
        html += "</body></html>"
        doc = self.parser.fromstring(html)
        elements = self.parser.getElementsByTags(doc, ["p", "a", "strong"])
        self.assertEqual(len(elements), 5)

        # find childs within the first p
        p = self.parser.get_elements_by_tag(doc, tag="p")[0]
        elements = self.parser.getElementsByTags(p, ["p", "a", "strong"])
        self.assertEqual(len(elements), 2)

    @fail_after(CAMEL_CASE_DEPRICATION, "createElement")
    def test_create_element_old(self):  # TODO: currently there isn't one that tests this functionality directly
        self.assertTrue(True)

    @fail_after(CAMEL_CASE_DEPRICATION, "getComments")
    def test_get_comments_old(self):  # TODO: currently there isn't one that tests this functionality directly
        self.assertTrue(True)

    @fail_after(CAMEL_CASE_DEPRICATION, "getParent")
    def test_get_parent_old(self):  # TODO: currently there isn't one that tests this functionality directly
        self.assertTrue(True)

    @fail_after(CAMEL_CASE_DEPRICATION, "getTag")
    def test_get_tag_old(self):  # TODO: currently there isn't one that tests this functionality directly
        self.assertTrue(True)

    @fail_after(CAMEL_CASE_DEPRICATION, "getText")
    def test_get_text_old(self):  # TODO: currently there isn't one that tests this functionality directly
        self.assertTrue(True)

    @fail_after(CAMEL_CASE_DEPRICATION, "previousSiblings")
    def test_previous_siblings_old(self):  # TODO: currently there isn't one that tests this functionality directly
        self.assertTrue(True)

    @fail_after(CAMEL_CASE_DEPRICATION, "nextSibling")
    def test_next_sibling_old(self):  # TODO: currently there isn't one that tests this functionality directly
        self.assertTrue(True)

    @fail_after(CAMEL_CASE_DEPRICATION, "isTextNode")
    def test_is_text_node_old(self):  # TODO: currently there isn't one that tests this functionality directly
        self.assertTrue(True)

    @fail_after(CAMEL_CASE_DEPRICATION, "getAttribute")
    def test_get_attribute_old(self):  # TODO: currently there isn't one that tests this functionality directly
        self.assertTrue(True)

    @fail_after(CAMEL_CASE_DEPRICATION, "delAttribute")
    def test_del_attribute_old(self):
        html = self.get_html("parser/test1.html")
        doc = self.parser.fromstring(html)

        # find div element with class foo
        elements = self.parser.get_elements_by_tag(doc, tag="div", attr="class", value="foo")
        self.assertEqual(len(elements), 1)

        div = elements[0]
        # remove an unexistant attribute
        self.parser.del_attribute(div, attr="bla")
        # remove the attribute class
        self.parser.del_attribute(div, attr="class")

        # find div element with class foo
        elements = self.parser.get_elements_by_tag(doc, tag="div", attr="class", value="foo")
        self.assertEqual(len(elements), 0)

    @fail_after(CAMEL_CASE_DEPRICATION, "setAttribute")
    def test_set_attribute_old(self):  # TODO: currently there isn't one that tests this functionality directly
        self.assertTrue(True)

    @fail_after(CAMEL_CASE_DEPRICATION, "outerHtml")
    def test_outer_html_old(self):  # TODO: currently there isn't one that tests this functionality directly
        self.assertTrue(True)


class TestParser(ParserBase):
    pass


class TestSoupParser(ParserBase):
    def setUp(self):
        self.parser = ParserSoup
