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
import hashlib
import logging
import os
import base64

from PIL import Image

from goose3.utils.encoding import smart_str
from goose3.image import (ImageDetails, LocallyStoredImage)

LOG = logging.getLogger(__name__)


class ImageUtils(object):

    @classmethod
    def get_image_dimensions(cls, identify_program, path):
        # TODO: identify_program is not used
        image_details = ImageDetails()
        try:
            # workaround to force the file to actually be closed by Pillow
            with open(path, 'rb') as img_file:
                with Image.open(img_file) as image:
                    image_details.set_mime_type(image.format)
                    width, height = image.size
            image_details.set_width(width)
            image_details.set_height(height)
        except OSError:
            image_details.set_mime_type('NA')
            LOG.exception("Cannot identify image file")
        except Exception as ex:
            # TODO: Should we look into other possible exceptions?
            image_details.set_mime_type('NA')
            LOG.exception("Exception: {}".format(ex))
        return image_details

    @classmethod
    def store_image(cls, http_client, link_hash, src, config):
        """\
        Writes an image src http string to disk as a temporary file
        and returns the LocallyStoredImage object
        that has the info you should need on the image
        """
        # check for a cache hit already on disk
        image = cls.read_localfile(link_hash, src, config)
        if image:
            return image

        # no cache found; do something else

        # parse base64 image
        if src.startswith('data:image'):
            image = cls.write_localfile_base64(link_hash, src, config)
            return image

        # download the image
        data = http_client.fetch(src)
        if data:
            image = cls.write_localfile(data, link_hash, src, config)
            if image:
                return image

        return None

    @classmethod
    def get_mime_type(cls, image_details):
        mime_type = image_details.get_mime_type().lower()
        mimes = {
            'png': '.png',
            'jpg': '.jpg',
            'jpeg': '.jpg',
            'gif': '.gif',
        }
        return mimes.get(mime_type, 'NA')

    @classmethod
    def read_localfile(cls, link_hash, src, config):
        local_image_name = cls.get_localfile_name(link_hash, src, config)
        if os.path.isfile(local_image_name):
            identify = config.imagemagick_identify_path
            image_details = cls.get_image_dimensions(identify, local_image_name)
            file_extension = cls.get_mime_type(image_details)
            filesize = os.path.getsize(local_image_name)
            return LocallyStoredImage(src=src,
                                      local_filename=local_image_name,
                                      link_hash=link_hash,
                                      size=filesize,
                                      file_extension=file_extension,
                                      height=image_details.get_height(),
                                      width=image_details.get_width())
        return None

    @classmethod
    def write_localfile(cls, entity, link_hash, src, config):
        local_path = cls.get_localfile_name(link_hash, src, config)
        with open(local_path, 'wb') as fobj:
            fobj.write(entity)
        return cls.read_localfile(link_hash, src, config)

    @classmethod
    def write_localfile_base64(cls, link_hash, src, config):
        data = src[src.find('base64,') + 7:]
        entity = bytes(base64.b64decode(data))
        return cls.write_localfile(entity, link_hash, src, config)

    @classmethod
    def get_localfile_name(cls, link_hash, src, config):
        image_hash = hashlib.md5(smart_str(src)).hexdigest()
        return os.path.join(config.local_storage_path, '%s_%s' % (link_hash, image_hash))

    @classmethod
    def clean_src_string(cls, src):
        return src.replace(" ", "%20")

    @classmethod
    def fetch(cls, http_client, src):
        return http_client.fetch(src)
