# -*- coding: utf-8 -*-
import datetime

from decimal import Decimal


class DjangoUnicodeDecodeError(UnicodeDecodeError):
    def __init__(self, obj, *args):
        self.obj = obj
        UnicodeDecodeError.__init__(self, *args)

    def __str__(self):
        original = UnicodeDecodeError.__str__(self)
        return '%s. You passed in %r (%s)' % (original, self.obj, type(self.obj))


class StrAndUnicode(object):
    """
    A class whose __str__ returns its __unicode__ as a UTF-8 bytestring.

    Useful as a mix-in.
    """
    # TODO: Unused class that I recommend we remove!
    def __str__(self):
        return self.__unicode__().encode('utf-8')


def smart_unicode(string, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Returns a unicode object representing 's'. Treats bytestrings using the
    'encoding' codec.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    # if isinstance(s, Promise):
    #     # The input is the result of a gettext_lazy() call.
    #     return s
    return force_unicode(string, encoding, strings_only, errors)


def is_protected_type(obj):
    """Determine if the object instance is of a protected type.

    Objects of protected types are preserved as-is when passed to
    force_unicode(strings_only=True).
    """
    return isinstance(obj, (type(None), int,
                            datetime.datetime, datetime.date, datetime.time,
                            float, Decimal))


def force_unicode(string, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Similar to smart_unicode, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    # Handle the common case first, saves 30-40% in performance when s
    # is an instance of unicode. This function gets called often in that
    # setting.
    if isinstance(string, str):
        return string
    if strings_only and is_protected_type(string):
        return string
    try:
        if not isinstance(string, str):
            if hasattr(string, '__unicode__'):
                string = string.__unicode__()
            else:
                try:
                    string = str(string, encoding, errors)
                except UnicodeEncodeError:
                    if not isinstance(string, Exception):
                        raise
                    # If we get to here, the caller has passed in an Exception
                    # subclass populated with non-ASCII data without special
                    # handling to display as a string. We need to handle this
                    # without raising a further exception. We do an
                    # approximation to what the Exception's standard str()
                    # output should be.
                    string = ' '.join([force_unicode(arg, encoding,
                                                     strings_only,
                                                     errors) for arg in string])
        elif not isinstance(string, str):
            # Note: We use .decode() here, instead of unicode(s, encoding,
            # errors), so that if s is a SafeString, it ends up being a
            # SafeUnicode at the end.
            string = string.decode(encoding, errors)
    except UnicodeDecodeError as ex:
        if not isinstance(string, Exception):
            raise DjangoUnicodeDecodeError(string, *ex.args)
        else:
            # If we get to here, the caller has passed in an Exception
            # subclass populated with non-ASCII bytestring data without a
            # working unicode method. Try to handle this without raising a
            # further exception by individually forcing the exception args
            # to unicode.
            string = ' '.join([force_unicode(arg, encoding, strings_only,
                                             errors) for arg in string])
    return string


def smart_str(string, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Returns a bytestring version of 's', encoded as specified in 'encoding'.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and isinstance(string, (type(None), int)):
        return string
    # if isinstance(s, Promise):
    #     return unicode(s).encode(encoding, errors)
    if isinstance(string, str):
        try:
            return string.encode(encoding, errors)
        except UnicodeEncodeError:
            return string.encode('utf-8', errors)
    elif not isinstance(string, bytes):
        try:
            return str(string).encode(encoding, errors)
        except UnicodeEncodeError:
            if isinstance(string, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return ' '.join([smart_str(arg, encoding, strings_only,
                                           errors) for arg in string])
            return str(string).encode(encoding, errors)
    else:
        return string
