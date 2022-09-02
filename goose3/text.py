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
import os
import re
import string
import warnings

from goose3.utils import FileHelper
from goose3.utils.encoding import (smart_unicode, smart_str, DjangoUnicodeDecodeError)


SPACE_SYMBOLS = re.compile(r'[\s\xa0\t]')
TABSSPACE = re.compile(r'[\s\t]+')


def get_encodings_from_content(content):
    """
    Code from:
    https://github.com/sigmavirus24/requests-toolbelt/blob/master/requests_toolbelt/utils/deprecated.py
    Return encodings from given content string.
    :param content: string to extract encodings from.
    """
    if isinstance(content, bytes):
        find_charset = re.compile(
            br'<meta.*?charset=["\']*[^a-zA-z0-9]*([a-zA-Z0-9\-_]+?)[^a-zA-z0-9]* *?["\'>]', flags=re.I
        ).findall

        find_xml = re.compile(
            br'^<\?xml.*?encoding=["\']*([a-zA-Z0-9\-_]+?) *?["\'>]'
        ).findall
        return [encoding.decode('utf-8') for encoding in
                find_charset(content) + find_xml(content)]
    else:
        find_charset = re.compile(
            r'<meta.*?charset=["\']*[^a-zA-z0-9]*([a-zA-Z0-9\-_]+?)[^a-zA-z0-9]* *?["\'>]', flags=re.I
        ).findall

        find_xml = re.compile(
            r'^<\?xml.*?encoding=["\']*([a-zA-Z0-9\-_]+?) *?["\'>]'
        ).findall
        return find_charset(content) + find_xml(content)


def innerTrim(value):
    if isinstance(value, str):
        # remove tab and white space
        value = re.sub(TABSSPACE, ' ', value)
        value = ''.join(value.splitlines())
        return value.strip()
    return ''


def encodeValue(value):
    string_org = value
    try:
        value = smart_unicode(value)
    except (UnicodeEncodeError, DjangoUnicodeDecodeError):
        value = smart_str(value)
    except Exception:
        value = string_org
    return value


class WordStats(object):

    def __init__(self):
        # total number of stopwords or
        # good words that we can calculate
        self.stop_word_count = 0

        # total number of words on a node
        self.word_count = 0

        # holds an actual list
        # of the stop words we found
        self.stop_words = []

    def get_stop_words(self):
        return self.stop_words

    def set_stop_words(self, words):
        self.stop_words = words

    def get_stopword_count(self):
        return self.stop_word_count

    def set_stopword_count(self, wordcount):
        self.stop_word_count = wordcount

    def get_word_count(self):
        return self.word_count

    def set_word_count(self, cnt):
        self.word_count = cnt


class StopWords(object):
    _cached_stop_words = {}

    def __init__(self, language='en'):
        if language not in self._cached_stop_words:
            path = os.path.join('text', 'stopwords-%s.txt' % language)
            try:
                content = FileHelper.loadResourceFile(path)
                word_list = content.splitlines()
            except IOError:
                word_list = []
            self._cached_stop_words[language] = set(word_list)
        self._stop_words = self._cached_stop_words[language]

    @staticmethod
    def remove_punctuation(content):
        # code taken form
        # http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
        if not isinstance(content, str):
            content = content.decode('utf-8')
        tbl = dict.fromkeys(ord(x) for x in string.punctuation)
        return content.translate(tbl)

    @staticmethod
    def candidate_words(stripped_input):
        return re.split(SPACE_SYMBOLS, stripped_input)

    def get_stopword_count(self, content):
        if not content:
            return WordStats()
        stats = WordStats()
        stripped_input = self.remove_punctuation(content)
        candidate_words = self.candidate_words(stripped_input)
        overlapping_stopwords = []
        i = 0
        for word in candidate_words:
            i += 1
            if word.lower() in self._stop_words:
                overlapping_stopwords.append(word.lower())

        stats.set_word_count(i)
        stats.set_stopword_count(len(overlapping_stopwords))
        stats.set_stop_words(overlapping_stopwords)
        return stats


class StopWordsChinese(StopWords):
    """
    Chinese segmentation
    """
    def __init__(self, language='zh'):
        # force zh languahe code
        super(StopWordsChinese, self).__init__(language='zh')

    @staticmethod
    def candidate_words(stripped_input):
        # jieba build a tree that takes sometime
        # avoid building the tree if we don't use
        # chinese language
        try:
            import jieba
        except ImportError:
            warnings.warn("jieba is not installed. To use Chinese, one must install the jieba package")
            return []
        return jieba.cut(stripped_input, cut_all=True)


class StopWordsArabic(StopWords):
    """
    Arabic segmentation
    """
    def __init__(self, language='ar'):
        # force ar languahe code
        super(StopWordsArabic, self).__init__(language='ar')

    @staticmethod
    def remove_punctuation(content):
        return content

    @staticmethod
    def candidate_words(stripped_input):
        try:
            import nltk
        except ImportError:
            warnings.warn("NLTK is not installed. To use Arabic, one must install the nltk package")
            return []
        stemmer = nltk.stem.isri.ISRIStemmer()
        words = []
        for word in nltk.tokenize.wordpunct_tokenize(stripped_input):
            words.append(stemmer.stem(word))
        return words


class StopWordsKorean(StopWords):
    """
    Korean segmentation
    """
    def __init__(self, language='ko'):
        super(StopWordsKorean, self).__init__(language='ko')

    def get_stopword_count(self, content):
        if not content:
            return WordStats()
        stats = WordStats()
        stripped_input = self.remove_punctuation(content)
        candidate_words = self.candidate_words(stripped_input)
        overlapping_stopwords = []
        i = 0
        for _ in candidate_words:
            i += 1
            for stop_word in self._stop_words:
                overlapping_stopwords.append(stop_word)

        stats.set_word_count(i)
        stats.set_stopword_count(len(overlapping_stopwords))
        stats.set_stop_words(overlapping_stopwords)
        return stats
