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
import os
import tempfile
import unittest

from goose3 import Goose


class TestTempDir(unittest.TestCase):
    def test_tmp_defaut(self):
        g = Goose()
        default_local_storage_path = os.path.join(tempfile.gettempdir(), "goose")
        self.assertEqual(g.config.local_storage_path, default_local_storage_path)

    def test_tmp_overwritten(self):
        path = "/tmp/goose"
        g = Goose({"local_storage_path": path})
        self.assertEqual(g.config.local_storage_path, path)
