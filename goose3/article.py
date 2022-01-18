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


class Article(object):

    def __init__(self):
        self._title = ""
        self._cleaned_text = ""
        self._meta_description = ""
        self._meta_lang = ""
        self._meta_favicon = ""
        self._meta_keywords = ""
        self._meta_encoding = []
        self._canonical_link = ""
        self._domain = ""
        self._top_node = None
        self._top_image = None
        self._tags = []
        self._opengraph = {}
        self._tweets = []
        self._movies = []
        self._links = []
        self._authors = []
        self._final_url = ""
        self._link_hash = ""
        self._raw_html = ""
        self._schema = None
        self._doc = None
        self._raw_doc = None
        self._publish_date = None
        self._publish_datetime_utc = None
        self._additional_data = {}

    @property
    def title(self):
        ''' str: Title extracted from the HTML source

            Note:
                Read only '''
        return self._title

    @property
    def cleaned_text(self):
        ''' str: Cleaned text of the article without HTML tags; most commonly desired property

            Note:
                Read only '''
        return self._cleaned_text

    @property
    def meta_description(self):
        ''' str: Contents of the meta-description field from the HTML source

            Note:
                Read only '''
        return self._meta_description

    @property
    def meta_lang(self):
        ''' str: Contents of the meta-lang field from the HTML source

            Note:
                Read only '''
        return self._meta_lang

    @property
    def meta_favicon(self):
        ''' str: Contents of the meta-favicon field from the HTML source

            Note:
                Read only '''
        return self._meta_favicon

    @property
    def meta_keywords(self):
        ''' str: Contents of the meta-keywords field from the HTML source

            Note:
                Read only '''
        return self._meta_keywords

    @property
    def meta_encoding(self):
        ''' str: Contents of the encoding/charset field from the HTML source

            Note:
                Read only '''
        return self._meta_encoding

    @property
    def canonical_link(self):
        ''' str: The canonical link of the article if found in the meta data

            Note:
                Read only '''
        return self._canonical_link

    @property
    def domain(self):
        ''' str: Domain of the article parsed

            Note:
                Read only '''
        return self._domain

    @property
    def top_node(self):
        ''' etree: The top Element that is a candidate for the main body of the article

            Note:
                Read only '''
        return self._top_node

    @property
    def top_image(self):
        ''' Image: The top image object that likely represents the article

            Returns:
                Image: See more information on the goose3.Image class
            Note:
                Read only '''
        return self._top_image

    @property
    def tags(self):
        ''' list(str): List of article tags (non-metadata tags)

            Note:
                Read only '''
        return self._tags

    @property
    def opengraph(self):
        ''' dict: All opengraph tag data

            Note:
                Read only '''
        return self._opengraph

    @property
    def tweets(self):
        ''' list(str): A listing of embeded tweets in the article

            Note:
                Read only '''
        return self._tweets

    @property
    def movies(self):
        ''' list(Video): A listing of all videos within the article such as
            YouTube or Vimeo

            Returns:
                list(Video):  See more information on the goose3.Video class
            Note:
                Read only '''
        return self._movies

    @property
    def links(self):
        ''' list(str): A listing of URL links within the article

            Note:
                Read only '''
        return self._links

    @property
    def authors(self):
        ''' list(str): A listing of authors as parsed from the meta tags

            Note:
                Read only '''
        return self._authors

    @property
    def final_url(self):
        ''' str: The URL that was used to pull and parsed; `None` if raw_html was used
            and no url element was found.

            Note:
                Read only '''
        return self._final_url

    @property
    def link_hash(self):
        ''' str: The hash of the final url to be used for various identification tasks

            Note:
                Read only '''
        return self._link_hash

    @property
    def raw_html(self):
        ''' str: The HTML represented as a string

            Note:
                Read only '''
        return self._raw_html

    @property
    def doc(self):
        ''' etree: lxml document that is being processed

            Note:
                Read only '''
        return self._doc

    @property
    def raw_doc(self):
        ''' etree: Original, uncleaned, and untouched lxml document to be processed

            Note:
                Read only '''
        return self._raw_doc

    @property
    def schema(self):
        ''' dict: All schema tag data

            Note:
                Read only '''
        return self._schema

    @property
    def publish_date(self):
        ''' str: The date the article was published based on meta tag extraction

            Note:
                Read only '''
        return self._publish_date

    @property
    def publish_datetime_utc(self):
        ''' datetime.datetime: The date time version of the published date based on meta tag extraction \
            in the UTC timezone, if timezone information is known

            Note:
                Read only '''
        return self._publish_datetime_utc

    @property
    def additional_data(self):
        ''' dict: A property bucket for consumers of goose3 to store custom data extractions

            Note:
                Read only '''
        return self._additional_data

    @property
    def infos(self):
        ''' dict: The summation of all data available about the extracted article

            Note:
                Read only '''
        data = {
            "meta": {
                "description": self.meta_description,
                "lang": self.meta_lang,
                "keywords": self.meta_keywords,
                "favicon": self.meta_favicon,
                "canonical": self.canonical_link,
                "encoding": self.meta_encoding
            },
            "image": None,
            "domain": self.domain,
            "title": self.title,
            "cleaned_text": self.cleaned_text,
            "opengraph": self.opengraph,
            "tags": self.tags,
            "tweets": self.tweets,
            "movies": [],
            "links": self.links,
            "authors": self.authors,
            "publish_date": self.publish_date
        }

        # image
        if self.top_image is not None:
            data['image'] = {
                'url': self.top_image.src,
                'width': self.top_image.width,
                'height': self.top_image.height,
                'type': 'image'
            }

        # movies
        for movie in self.movies:
            data['movies'].append({
                'embed_type': movie.embed_type,
                'provider': movie.provider,
                'width': movie.width,
                'height': movie.height,
                'embed_code': movie.embed_code,
                'src': movie.src,
            })

        return data
