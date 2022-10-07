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
import functools
import pkgutil
import time
import typing
import warnings
from typing import Union

from goose3.utils.constants import UINT64_T_MAX

KeyT = Union[str, bytes]


class FileHelper:
    @classmethod
    def load_resource_file(cls, filename):
        try:
            return pkgutil.get_data("goose3", filename).decode("utf-8")
        except OSError as exc:
            raise OSError(f"Couldn't open file '{filename}' - {exc}") from exc


class ParsingCandidate:
    def __init__(self, url_string: str, link_hash: str):
        self.url = url_string
        self.link_hash = link_hash


class RawHelper:
    @classmethod
    def get_parsing_candidate(cls, url: str, raw_html: str) -> ParsingCandidate:
        if isinstance(raw_html, str):
            raw_html = raw_html.encode("utf-8")
        link_hash = f"{fnv_1a(raw_html)}.{time.time()}"
        return ParsingCandidate(url, link_hash)


class URLHelper:
    @classmethod
    def get_parsing_candidate(cls, url_to_crawl: str) -> ParsingCandidate:
        # replace shebang is urls
        if "#!" in url_to_crawl:
            final_url = url_to_crawl.replace("#!", "?_escaped_fragment_=")
        else:
            final_url = url_to_crawl

        # url is only for calculating the link_hash
        url = final_url.encode("utf-8") if isinstance(final_url, str) else final_url

        link_hash = f"{fnv_1a(url)}.{time.time()}"
        return ParsingCandidate(final_url, link_hash)


class StringReplacement:
    def __init__(self, pattern, replace_with):
        self.pattern = pattern
        self.replace_with = replace_with

    def replace_all(self, string):
        if not string:
            return ""
        return string.replace(self.pattern, self.replace_with)


class ReplaceSequence:
    def __init__(self):
        self.replacements = []

    # @classmethod
    def create(self, first_pattern, replace_with=None):
        result = StringReplacement(first_pattern, replace_with or "")
        self.replacements.append(result)
        return self

    def append(self, pattern, replace_with=None):
        return self.create(pattern, replace_with)

    def replace_all(self, string):
        if not string:
            return ""

        mutated_string = string

        for itm in self.replacements:
            mutated_string = itm.replace_all(mutated_string)
        return mutated_string


def fnv_1a(key: KeyT, seed: int = 0) -> str:
    """Pure python implementation of the 64 bit fnv-1a hash
    Args:
        key (str): The element to be hashed
        seed (int): Add a seed to the initial starting point (0 means no seed)
    Returns:
        str: 64-bit hashed representation of key
    Note:
        Uses the lower 64 bits when overflows occur"""
    max64mod = UINT64_T_MAX + 1
    hval = (14695981039346656037 + (31 * seed)) % max64mod
    fnv_64_prime = 1099511628211
    tmp = list(key) if not isinstance(key, str) else list(map(ord, key))
    for t_str in tmp:
        hval ^= t_str
        hval *= fnv_64_prime
        hval %= max64mod
    # Remove the leading "0x".
    return hex(hval)[2:]


def deprecated(message: str = "") -> typing.Callable:
    """A simplistic decorator to mark functions as deprecated. The function
    will pass a message to the user on the first use of the function

    Args:
        message (str): The message to display if the function is deprecated
    """

    def decorator_wrapper(func):
        @functools.wraps(func)
        def function_wrapper(*args, **kwargs):
            func_name = func.__name__
            if func_name not in function_wrapper.deprecated_items:
                msg = f"Function {func.__name__} is now deprecated! {message}"
                warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
                function_wrapper.deprecated_items.add(func_name)

            return func(*args, **kwargs)

        # set this up the first time the decorator is called
        function_wrapper.deprecated_items = set()

        return function_wrapper

    return decorator_wrapper
