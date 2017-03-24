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
from imp import load_source

from setuptools import setup

version = load_source("version", os.path.join("goose3", "version.py"))

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Other Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet',
    'Topic :: Utilities',
    'Topic :: Software Development :: Libraries :: Python Modules']

description = "Html Content / Article Extractor, web scrapping for Python3"

# read long description
try:
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
        long_description = f.read()
except Exception:
    long_description = description

setup(name='goose3',
      version=version.__version__,
      description=description,
      long_description=long_description,
      keywords='scrapping, extractor, web scrapping',
      classifiers=CLASSIFIERS,
      maintainer='Mahmoud Lababidi',
      maintainer_email='lababidi+py@gmail.com',
      url='https://github.com/goose3/goose3',
      license='Apache',
      packages=['goose3'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['Pillow', 'lxml', 'cssselect', 'jieba', 'beautifulsoup4', 'nltk', 'six'],
      test_requires=['nose', 'requests_mock'],
      test_suite="tests"
      )
