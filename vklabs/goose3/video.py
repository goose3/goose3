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


class Video(object):
    """\
    Video object
    """

    def __init__(self):

        # type of embed
        # embed, object, iframe
        self._embed_type = None

        # video provider name
        self._provider = None

        # width
        self._width = None

        # height
        self._height = None

        # embed code
        self._embed_code = None

        # src
        self._src = None

    @property
    def embed_type(self):
        ''' str: The type of embeding such as embed, object, or iframe

            Note:
                Read only '''
        return self._embed_type

    @property
    def provider(self):
        ''' str: The video provider

            Note:
                Read only '''
        return self._provider

    @property
    def width(self):
        ''' int: The video width in pixels

            Note:
                Read only '''
        return self._width

    @property
    def height(self):
        ''' int: The video height in pixels

            Note:
                Read only '''
        return self._height

    @property
    def embed_code(self):
        ''' str: The embed code of the video

            Note:
                Read only '''
        return self._embed_code

    @property
    def src(self):
        ''' str: The URL source of the video

            Note:
                Read only '''
        return self._src
