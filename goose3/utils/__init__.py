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
import time
import hashlib
import re
import os
import codecs

from .. version import install_location


class FileHelper(object):

    @classmethod
    def load_resource_file(cls, filename):
        if not os.path.isabs('filename'):
            dirpath = os.path.dirname(install_location)
            path = os.path.join(dirpath, 'resources', filename)
        else:
            path = filename
        try:
            with codecs.open(path, 'r', 'utf-8') as fp:
                content = fp.read()
            return content
        except IOError:
            raise IOError("Couldn't open file {}".format(path))


class ParsingCandidate(object):

    def __init__(self, url_string, link_hash):
        self.url_string = self.url = url_string
        self.link_hash = link_hash


class RawHelper(object):
    @classmethod
    def get_parsing_candidate(cls, url, raw_html):
        if isinstance(raw_html, str):
            raw_html = raw_html.encode('utf-8')
        link_hash = '{}.{}'.format(hashlib.md5(raw_html).hexdigest(), time.time())
        return ParsingCandidate(url, link_hash)


class URLHelper(object):
    @classmethod
    def get_parsing_candidate(cls, url_to_crawl):
        # replace shebang is urls
        if '#!' in url_to_crawl:
            final_url = url_to_crawl.replace('#!', '?_escaped_fragment_=')
        else:
            final_url = url_to_crawl
        link_hash = '{}.{}'.format(hashlib.md5(final_url.encode("utf-8")).hexdigest(), time.time())
        return ParsingCandidate(final_url, link_hash)


class StringReplacement(object):

    def __init__(self, pattern, replaceWith):
        self.pattern = pattern
        self.replaceWith = replaceWith

    def replaceAll(self, string):
        if not string:
            return ''
        return string.replace(self.pattern, self.replaceWith)


class ReplaceSequence(object):

    def __init__(self):
        self.replacements = []

    def create(self, firstPattern, replaceWith=None):
        result = StringReplacement(firstPattern, replaceWith or '')
        self.replacements.append(result)
        return self

    def append(self, pattern, replaceWith=None):
        return self.create(pattern, replaceWith)

    def replaceAll(self, string):
        if not string:
            return ''

        mutated_string = string

        for reps in self.replacements:
            mutated_string = reps.replaceAll(mutated_string)
        return mutated_string
