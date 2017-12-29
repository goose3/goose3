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

import lxml.html
from lxml import etree

from goose3.text import innerTrim, encodeValue, get_encodings_from_content, smart_str


class Parser(object):

    @classmethod
    def xpath_re(cls, node, expression):
        regexp_namespace = "http://exslt.org/regular-expressions"
        items = node.xpath(expression, namespaces={'re': regexp_namespace})
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
        encoding = encoding and encoding[0] or None
        if not encoding:
            html = encodeValue(html)
            doc = lxml.html.fromstring(html)
        else:
            html = smart_str(html, encoding=encoding)
            parser = lxml.html.HTMLParser(encoding=encoding)
            doc = lxml.html.fromstring(html, parser=parser)
        return doc

    @classmethod
    def nodeToString(cls, node):
        return etree.tostring(node, encoding=str)

    @classmethod
    def replaceTag(cls, node, tag):
        node.tag = tag

    @classmethod
    def stripTags(cls, node, *tags):
        etree.strip_tags(node, *tags)

    @classmethod
    def getElementById(cls, node, idd):
        selector = '//*[@id="%s"]' % idd
        elems = node.xpath(selector)
        if elems:
            return elems[0]
        return None

    @classmethod
    def getElementsByTag(cls, node, tag=None, attr=None, value=None, childs=False):
        namespace = "http://exslt.org/regular-expressions"
        # selector = tag or '*'
        selector = 'descendant-or-self::%s' % (tag or '*')
        if attr and value:
            selector = '%s[re:test(@%s, "%s", "i")]' % (selector, attr, value)
        elems = node.xpath(selector, namespaces={"re": namespace})
        # remove the root node
        # if we have a selection tag
        if node in elems and (tag or childs):
            elems.remove(node)
        return elems

    @classmethod
    def appendChild(cls, node, child):
        node.append(child)

    @classmethod
    def childNodes(cls, node):
        return list(node)

    @classmethod
    def childNodesWithText(cls, node):
        root = node
        # create the first text node
        # if we have some text in the node
        if root.text:
            elm = lxml.html.HtmlElement()
            elm.text = root.text
            elm.tag = 'text'
            root.text = None
            root.insert(0, elm)
        # loop childs
        for _, elm in enumerate(list(root)):
            idx = root.index(elm)
            # don't process texts nodes
            if elm.tag == 'text':
                continue
            # create a text node for tail
            if elm.tail:
                tmp = cls.createElement(tag='text', text=elm.tail, tail=None)
                root.insert(idx + 1, tmp)
        return list(root)

    @classmethod
    def textToPara(cls, text):
        return cls.fromstring(text)

    @classmethod
    def getChildren(cls, node):
        return node.getchildren()

    @classmethod
    def getElementsByTags(cls, node, tags):
        selector = ','.join(tags)
        elems = cls.css_select(node, selector)
        # remove the root node
        # if we have a selection tag
        if node in elems:
            elems.remove(node)
        return elems

    @classmethod
    def createElement(cls, tag='p', text=None, tail=None):
        elm = lxml.html.HtmlElement()
        elm.tag = tag
        elm.text = text
        elm.tail = tail
        return elm

    @classmethod
    def getComments(cls, node):
        return node.xpath('//comment()')

    @classmethod
    def getParent(cls, node):
        return node.getparent()

    @classmethod
    def remove(cls, node):
        parent = node.getparent()
        if parent is not None:
            if node.tail:
                prev = node.getprevious()
                if prev is None:
                    if not parent.text:
                        parent.text = ''
                    parent.text += ' ' + node.tail
                else:
                    if not prev.tail:
                        prev.tail = ''
                    prev.tail += ' ' + node.tail
            node.clear()
            parent.remove(node)

    @classmethod
    def getTag(cls, node):
        return node.tag

    @classmethod
    def getText(cls, node):
        txts = [i for i in node.itertext()]
        return innerTrim(' '.join(txts).strip())

    @classmethod
    def previousSiblings(cls, node):
        nodes = []
        for _, val in enumerate(node.itersiblings(preceding=True)):
            nodes.append(val)
        return nodes

    @classmethod
    def previousSibling(cls, node):
        nodes = []
        for idx, val in enumerate(node.itersiblings(preceding=True)):
            nodes.append(val)
            if idx == 0:
                break
        return nodes[0] if nodes else None

    @classmethod
    def nextSibling(cls, node):
        nodes = []
        for idx, val in enumerate(node.itersiblings(preceding=False)):
            nodes.append(val)
            if idx == 0:
                break
        return nodes[0] if nodes else None

    @classmethod
    def isTextNode(cls, node):
        return True if node.tag == 'text' else False

    @classmethod
    def getAttribute(cls, node, attr=None):
        if attr:
            return node.attrib.get(attr, None)
        return attr

    @classmethod
    def delAttribute(cls, node, attr=None):
        if attr:
            _attr = node.attrib.get(attr, None)
            if _attr:
                del node.attrib[attr]

    @classmethod
    def setAttribute(cls, node, attr=None, value=None):
        if attr and value:
            node.set(attr, value)

    @classmethod
    def outerHtml(cls, node):
        tmp = node
        if tmp.tail:
            tmp = deepcopy(tmp)
            tmp.tail = None
        return cls.nodeToString(tmp)


class ParserSoup(Parser):

    @classmethod
    def fromstring(cls, html):
        from lxml.html import soupparser
        html = encodeValue(html)
        doc = soupparser.fromstring(html)
        return doc
