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
import re
from urllib.parse import urljoin, urlparse

from goose3.extractors import BaseExtractor
from goose3.text import get_encodings_from_content

RE_LANG = r"^[A-Za-z]{2}$"


class MetasExtractor(BaseExtractor):
    def get_domain(self):
        if self.article.final_url:
            o = urlparse(self.article.final_url)
            return o.hostname
        return None

    def get_favicon(self):
        """Extract the favicon from a website
        http://en.wikipedia.org/wiki/Favicon<link rel="shortcut icon" type="image/png" href="favicon.png" />
        <link rel="icon" type="image/png" href="favicon.png" />"""
        kwargs = {"tag": "link", "attr": "rel", "value": "icon"}
        meta = self.parser.get_elements_by_tag(self.article.doc, **kwargs)
        if meta:
            favicon = self.parser.get_attribute(meta[0], "href")
            return favicon
        return ""

    def get_canonical_link(self):
        """if the article has meta canonical link set in the url"""
        if self.article.final_url:
            kwargs = {"tag": "link", "attr": "rel", "value": "canonical"}
            meta = self.parser.get_elements_by_tag(self.article.doc, **kwargs)
            if meta is not None and len(meta) > 0:
                href = self.parser.get_attribute(meta[0], "href")
                if href:
                    href = href.strip()
                    o = urlparse(href)
                    if not o.hostname:
                        tmp = urlparse(self.article.final_url)
                        domain = f"{tmp.scheme}://{tmp.hostname}"
                        href = urljoin(domain, href)
                    return href
        return self.article.final_url

    def get_meta_lang(self):
        """Extract content language from meta"""
        # we have a lang attribute in html
        attr = self.parser.get_attribute(self.article.doc, attr="lang")
        if attr is None:
            # look up for a Content-Language in meta
            items = [
                {"tag": "meta", "attr": "http-equiv", "value": "content-language"},
                {"tag": "meta", "attr": "name", "value": "lang"},
            ]
            for item in items:
                meta = self.parser.get_elements_by_tag(self.article.doc, **item)
                if meta:
                    attr = self.parser.get_attribute(meta[0], attr="content")
                    break

        if attr:
            value = attr[:2]
            if re.search(RE_LANG, value):
                return value.lower()

        return None

    def get_meta_content(self, meta_name):
        """Extract a given meta content form document"""
        meta = self.parser.css_select(self.article.doc, meta_name)
        content = None

        if meta is not None and len(meta) > 0:
            content = self.parser.get_attribute(meta[0], "content")

        if content:
            return content.strip()

        return ""

    def get_meta_description(self):
        """if the article has meta description set in the source, use that"""
        return self.get_meta_content("meta[name=description]")

    def get_meta_keywords(self):
        """if the article has meta keywords set in the source, use that"""
        return self.get_meta_content("meta[name=keywords]")

    def get_meta_encoding(self):
        """Parse the meta encoding"""
        encoding = get_encodings_from_content(self.article.raw_html)
        return encoding[0] if encoding else None

    def extract(self):
        return {
            "description": self.get_meta_description(),
            "keywords": self.get_meta_keywords(),
            "lang": self.get_meta_lang(),
            "favicon": self.get_favicon(),
            "canonical": self.get_canonical_link(),
            "domain": self.get_domain(),
            "encoding": self.get_meta_encoding(),
        }
