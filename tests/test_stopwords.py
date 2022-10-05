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
import unittest

from goose3.text import StopWords, StopWordsKorean


class TestStopWordsBase(unittest.TestCase):
    def setUp(self):
        self.stopwords_class = StopWords
        self.lang = "en"

    def test_stop_words(self):
        # test that all the stopwords present in the paragraph are detected, and also
        # show that founds are valid

        text = "TextNode 1 - The Scala supported IDE is one of the few pain points of developers"
        text += " who want to start using Scala in their Java project."
        text += " On existing long term project developed by a team its hard to step in and introduce a new language"
        text += " that is not supported by the existing IDE."
        text += " On way to go about it is to hid the fact"
        text += " that you use Scala from the Java world by using one way dependency injection."
        text += " Still, if you wish to truly absorb Scala into your existing java environment"
        text += " then you'll soon introduced cross language dependencies."
        expected = [
            "the",
            "is",
            "one",
            "of",
            "the",
            "few",
            "of",
            "who",
            "want",
            "to",
            "using",
            "in",
            "their",
            "on",
            "by",
            "its",
            "to",
            "in",
            "and",
            "new",
            "that",
            "is",
            "not",
            "by",
            "the",
            "on",
            "way",
            "to",
            "go",
            "about",
            "it",
            "is",
            "to",
            "the",
            "that",
            "you",
            "use",
            "from",
            "the",
            "by",
            "using",
            "one",
            "way",
            "still",
            "if",
            "you",
            "wish",
            "to",
            "truly",
            "into",
            "your",
            "then",
            "soon",
        ]

        word_stats = self.stopwords_class(self.lang).get_stopword_count(text)

        self.assertEqual(word_stats.get_word_count(), 98)
        self.assertEqual(word_stats.get_stopword_count(), 53)
        self.assertCountEqual(word_stats.get_stop_words(), expected)
        self.assertListEqual(word_stats.get_stop_words(), expected)

        # check that founds are valid
        valid_stop_words = self.stopwords_class(self.lang)._stop_words
        for found_stop_word in word_stats.get_stop_words():
            self.assertIn(found_stop_word, valid_stop_words)


class TestStopWordsKorean(TestStopWordsBase):
    def setUp(self):
        self.stopwords_class = StopWordsKorean
        self.lang = "ko"

    def test_stop_words(self):
        text = "스칼라는 마틴 오더스키가 자바 제네릭 컴파일러를 개발하며 느꼈던 자바의 여러 가지 단점들을 근본적으로 수정하고,"
        text += " 추후 프로그램 언어 연구를 위한 연구 플랫폼으로 함께 사용하기 위하여 디자인한 언어이다."
        text += " 따라서 언뜻 보기에는 자바와 비슷해 보일지 모르나 여러가지 측면에서 더욱 발전된 형태를 가지고 있다."
        expected = [
            "라",
            "는",
            "가",
            "를",
            "며",
            "의",
            "여",
            "가",
            "을",
            "으로",
            "로",
            "하고",
            "고",
            "로",
            "를",
            "으로",
            "로",
            "께",
            "여",
            "이",
            "이다",
            "다",
            "라",
            "에",
            "에는",
            "는",
            "와",
            "나",
            "여",
            "가",
            "에",
            "에서",
            "를",
            "가",
            "고",
            "다",
        ]

        word_stats = self.stopwords_class(self.lang).get_stopword_count(text)

        self.assertEqual(word_stats.get_word_count(), 40)
        self.assertEqual(word_stats.get_stopword_count(), 36)
        self.assertCountEqual(word_stats.get_stop_words(), expected)
        self.assertListEqual(word_stats.get_stop_words(), expected)

        valid_stop_words = self.stopwords_class(self.lang)._stop_words
        for found_stop_word in word_stats.get_stop_words():
            self.assertIn(found_stop_word, valid_stop_words)
