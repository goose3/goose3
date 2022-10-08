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
import unittest

from goose3.configuration import Configuration
from goose3.image import Image, ImageDetails
from goose3.utils.images import ImageUtils

from .test_base import TestExtractionBase

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


class ImageExtractionTests(TestExtractionBase):
    def getConfig(self):
        config = Configuration()
        config.enable_image_fetching = True
        return config

    def assert_top_image(self, fields, expected_value, result_image):
        # test if the result value
        # is an Goose Image instance
        msg = "Result value is not a Goose Image instance"
        self.assertTrue(isinstance(result_image, Image), msg=msg)

        # expected image
        expected_image = Image()
        for k, v in list(expected_value.items()):
            setattr(expected_image, f"_{k}", v)
        msg = "Expected value is not a Goose Image instance"
        self.assertTrue(isinstance(expected_image, Image), msg=msg)

        # check
        msg = "Returned Image is not the one expected"
        self.assertIn(result_image.src, expected_image.src, msg=msg)

        fields = vars(expected_image)
        for k, v in list(fields.items()):
            msg = "Returned Image attribute '%s' is not the one expected" % k
            self.assertEqual(getattr(expected_image, k), getattr(result_image, k), msg=msg)

    def test_basic_image(self):
        article = self.getArticle()
        fields = ["top_image"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_base64_image(self):
        article = self.getArticle()
        fields = ["top_image"]
        self.runArticleAssertions(article=article, fields=fields)

    def _test_known_image_css(self, article):
        # check if we have an image in article.top_node
        images = self.parser.get_elements_by_tag(article.top_node, tag="img")
        self.assertEqual(len(images), 0)

        # we dont' have an image in article.top_node
        # check if the correct image was retrieved
        # using the known-image-css.txt
        fields = ["cleaned_text", "top_image"]
        self.runArticleAssertions(article=article, fields=fields)

    def test_known_image_name_parent(self):
        article = self.getArticle()
        self._test_known_image_css(article)

    def test_known_image_css_parent_class(self):
        article = self.getArticle()
        self._test_known_image_css(article)

    def test_known_image_css_parent_id(self):
        article = self.getArticle()
        self._test_known_image_css(article)

    def test_known_image_css_class(self):
        article = self.getArticle()
        self._test_known_image_css(article)

    def test_known_image_css_id(self):
        article = self.getArticle()
        self._test_known_image_css(article)

    def test_known_image_empty_src(self):
        "Tests that img tags for known image sources with empty src attributes are skipped."
        article = self.getArticle()
        self._test_known_image_css(article)

    def test_opengraph_tag(self):
        article = self.getArticle()
        self._test_known_image_css(article)

    def test_reportagenewsarticle(self):
        article = self.getArticle()
        self._test_known_image_css(article)


class ImageUtilsTests(unittest.TestCase):
    def setUp(self):
        self.path = f"{CURRENT_PATH}/data/images/50850547cc7310bc53e30e802c6318f1"
        self.expected_results = {"width": 476, "height": 317, "mime_type": "JPEG"}

    def test_utils_get_image_dimensions(self):
        image_detail = ImageUtils.get_image_dimensions(self.path)

        # test if we have an ImageDetails instance
        self.assertTrue(isinstance(image_detail, ImageDetails))

        # test image_detail attribute
        for k, v in list(self.expected_results.items()):
            self.assertEqual(getattr(image_detail, k), v)

    def test_detail(self):
        image_detail = ImageUtils.get_image_dimensions(self.path)

        # test if we have an ImageDetails instance
        self.assertTrue(isinstance(image_detail, ImageDetails))

        # test image_detail attribute
        for k, v in list(self.expected_results.items()):
            self.assertEqual(getattr(image_detail, k), v)

        # test image_detail get_ methode
        for k, v in list(self.expected_results.items()):
            attr = "get_%s" % k
            self.assertEqual(getattr(image_detail, attr)(), v)

        # test image_detail set_ methode
        expected_results = {"width": 10, "height": 10, "mime_type": "PNG"}

        for k, v in list(expected_results.items()):
            attr = "set_%s" % k
            getattr(image_detail, attr)(v)

        for k, v in list(expected_results.items()):
            attr = "get_%s" % k
            self.assertEqual(getattr(image_detail, attr)(), v)
