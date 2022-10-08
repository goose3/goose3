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
from copy import deepcopy

import lxml.html
from lxml import etree

from goose3.text import encode_value, get_encodings_from_content, inner_trim, smart_str
from goose3.utils import deprecated
from goose3.utils.constants import CAMEL_CASE_DEPRICATION


class Parser:
    @classmethod
    def xpath_re(cls, node, expression):
        regexp_namespace = "http://exslt.org/regular-expressions"
        items = node.xpath(expression, namespaces={"re": regexp_namespace})
        return items

    @classmethod
    def drop_tag(cls, nodes):
        if isinstance(nodes, list):
            for node in nodes:
                node.drop_tag()
        else:
            nodes.drop_tag()

    @classmethod
    def css_select(cls, node, selector):
        return node.cssselect(selector)

    @classmethod
    def fromstring(cls, html):
        encoding = get_encodings_from_content(html)
        encoding = encoding[0] if encoding else None
        if not encoding:
            html = encode_value(html)
            doc = lxml.html.fromstring(html)
        else:
            html = smart_str(html, encoding=encoding)
            parser = lxml.html.HTMLParser(encoding=encoding)
            doc = lxml.html.fromstring(html, parser=parser)
        return doc

    @classmethod
    def node_to_string(cls, node):
        return etree.tostring(node, encoding=str)

    @classmethod
    def replace_tag(cls, node, tag):
        node.tag = tag

    @classmethod
    def strip_tags(cls, node, *tags):
        etree.strip_tags(node, *tags)

    @classmethod
    def get_element_by_id(cls, node, idd):
        selector = f'//*[@id="{idd}"]'
        elems = node.xpath(selector)
        if elems:
            return elems[0]
        return None

    @classmethod
    def get_elements_by_tag(cls, node, tag=None, attr=None, value=None, childs=False):
        namespace = "http://exslt.org/regular-expressions"
        sel = tag or "*"
        selector = f"descendant-or-self::{sel}"
        if attr and value:
            selector = f'{selector}[re:test(@{attr}, "{value}", "i")]'
        elems = node.xpath(selector, namespaces={"re": namespace})
        # remove the root node
        # if we have a selection tag
        if node in elems and (tag or childs):
            elems.remove(node)
        return elems

    @classmethod
    def append_child(cls, node, child):
        node.append(child)

    @classmethod
    def child_nodes(cls, node):
        return list(node)

    @classmethod
    def child_nodes_with_text(cls, node):
        root = node
        # create the first text node
        # if we have some text in the node
        if root.text:
            elm = lxml.html.HtmlElement()
            elm.text = root.text
            elm.tag = "text"
            root.text = None
            root.insert(0, elm)
        # loop childs
        for _, elm in enumerate(list(root)):
            idx = root.index(elm)
            # don't process texts nodes
            if elm.tag == "text":
                continue
            # create a text node for tail
            if elm.tail:
                tmp = cls.create_element(tag="text", text=elm.tail, tail=None)
                root.insert(idx + 1, tmp)
        return list(root)

    @classmethod
    def text_to_para(cls, text):
        return cls.fromstring(text)

    @classmethod
    def get_children(cls, node):
        return node.getchildren()

    @classmethod
    def get_elements_by_tags(cls, node, tags):
        selector = ",".join(tags)
        elems = cls.css_select(node, selector)
        # remove the root node
        # if we have a selection tag
        if node in elems:
            elems.remove(node)
        return elems

    @classmethod
    def create_element(cls, tag="p", text=None, tail=None):
        elm = lxml.html.HtmlElement()
        elm.tag = tag
        elm.text = text
        elm.tail = tail
        return elm

    @classmethod
    def get_comments(cls, node):
        return node.xpath("//comment()")

    @classmethod
    def get_parent(cls, node):
        return node.getparent()

    @classmethod
    def remove(cls, node):
        parent = node.getparent()
        if parent is not None:
            if node.tail:
                prev = node.getprevious()
                if prev is None:
                    if not parent.text:
                        parent.text = ""
                    parent.text += " " + node.tail
                else:
                    if not prev.tail:
                        prev.tail = ""
                    prev.tail += " " + node.tail
            node.clear()
            parent.remove(node)

    @classmethod
    def get_tag(cls, node):
        return node.tag

    @classmethod
    def get_text(cls, node):
        return inner_trim(" ".join(node.itertext()).strip())

    @classmethod
    def previous_siblings(cls, node):
        nodes = []
        for _, val in enumerate(node.itersiblings(preceding=True)):
            nodes.append(val)
        return nodes

    @classmethod
    def previous_sibling(cls, node):
        nodes = []
        for idx, val in enumerate(node.itersiblings(preceding=True)):
            nodes.append(val)
            if idx == 0:
                break
        return nodes[0] if nodes else None

    @classmethod
    def next_sibling(cls, node):
        nodes = []
        for idx, val in enumerate(node.itersiblings(preceding=False)):
            nodes.append(val)
            if idx == 0:
                break
        return nodes[0] if nodes else None

    @classmethod
    def is_text_node(cls, node):
        return node.tag == "text"

    @classmethod
    def get_attribute(cls, node, attr=None):
        if attr:
            return node.attrib.get(attr, None)
        return attr

    @classmethod
    def del_attribute(cls, node, attr=None):
        if attr:
            _attr = node.attrib.get(attr, None)
            if _attr:
                del node.attrib[attr]

    @classmethod
    def set_attribute(cls, node, attr=None, value=None):
        if attr and value:
            node.set(attr, value)

    @classmethod
    def outer_html(cls, node):
        tmp = node
        if tmp.tail:
            tmp = deepcopy(tmp)
            tmp.tail = None
        return cls.node_to_string(tmp)

    # Aliases to previous names
    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use node_to_string instead")
    def nodeToString(cls, node):
        return cls.node_to_string(node)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use replace_tag instead")
    def replaceTag(cls, node, tag):
        return cls.replace_tag(node, tag)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use strip_tags instead")
    def stripTags(cls, node, *tags):
        return cls.strip_tags(node, tags)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use get_element_by_id instead")
    def getElementById(cls, node, idd):
        return cls.get_element_by_id(node, idd)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use get_elements_by_tag instead")
    def getElementsByTag(cls, node, tag=None, attr=None, value=None, childs=False):
        return cls.get_elements_by_tag(node, tag, attr, value, childs)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use append_child instead")
    def appendChild(cls, node, child):
        cls.append_child(node, child)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use child_nodes instead")
    def childNodes(cls, node):
        return cls.child_nodes(node)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use child_nodes_with_text instead")
    def childNodesWithText(cls, node):
        return cls.child_nodes_with_text(node)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use text_to_para instead")
    def textToPara(cls, text):
        return cls.text_to_para(text)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use get_children instead")
    def getChildren(cls, node):
        return cls.get_children(node)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use get_elements_by_tags instead")
    def getElementsByTags(cls, node, tags):
        return cls.get_elements_by_tags(node, tags)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use create_element instead")
    def createElement(cls, tag="p", text=None, tail=None):
        return cls.create_element(tag, text, tail)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use get_comments instead")
    def getComments(cls, node):
        return cls.get_comments(node)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use get_parent instead")
    def getParent(cls, node):
        return cls.get_parent(node)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use get_tag instead")
    def getTag(cls, node):
        return cls.get_tag(node)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use get_text instead")
    def getText(cls, node):
        return cls.get_text(node)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use previous_siblings instead")
    def previousSiblings(cls, node):
        return cls.previous_siblings(node)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use previous_sibling instead")
    def previousSibling(cls, node):
        return cls.previous_sibling(node)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use next_sibling instead")
    def nextSibling(cls, node):
        return cls.next_sibling(node)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use is_text_node instead")
    def isTextNode(cls, node):
        return cls.is_text_node(node)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use get_attribute instead")
    def getAttribute(cls, node, attr=None):
        return cls.get_attribute(node, attr)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use del_attribute instead")
    def delAttribute(cls, node, attr=None):
        cls.del_attribute(node, attr)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use set_attribute instead")
    def setAttribute(cls, node, attr=None, value=None):
        cls.set_attribute(node, attr, value)

    @classmethod
    @deprecated(f"Deprecated and to be removed in v{CAMEL_CASE_DEPRICATION}; use outer_html instead")
    def outerHtml(cls, node):
        return cls.outer_html(node)


class ParserSoup(Parser):
    @classmethod
    def fromstring(cls, html):
        from lxml.html import soupparser

        html = encode_value(html)
        doc = soupparser.fromstring(html)
        return doc
