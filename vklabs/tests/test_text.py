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
import unittest

from vklabs.goose3.text import get_encodings_from_content


class TestText(unittest.TestCase):

    def test_get_encodings_from_content_with_trail_spaces(self):
        self.assertEqual(
            get_encodings_from_content(
                '<meta charset=utf-8 " />'),
            ['utf-8']
        )
        self.assertEqual(
            get_encodings_from_content(
                '<meta http-equiv="content-type" content="text/html; charset=utf-8 " />'),
            ['utf-8']
        )
        self.assertEqual(
            get_encodings_from_content(
                '<meta http-equiv="content-type" content="text/html; charset=utf-8    " />'),
            ['utf-8']
        )
        self.assertEqual(
            get_encodings_from_content(
                b'<meta http-equiv="content-type" content="text/html; charset=utf-8 " />'),
            ['utf-8']
        )

    def test_get_encodings_from_content_with_out_trail_spaces(self):
        self.assertEqual(
            get_encodings_from_content(
                '<meta http-equiv="content-type" content="text/html; charset=utf-8" />'),
            ['utf-8']
        )
        self.assertEqual(
            get_encodings_from_content(
                b'<meta http-equiv="content-type" content="text/html; charset=utf-8" />'),
            ['utf-8']
        )
