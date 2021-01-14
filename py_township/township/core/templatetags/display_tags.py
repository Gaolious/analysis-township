# -*- coding: utf-8 -*-
"""
Copied from https://github.com/django-oscar/django-oscar/
blob/master/src/oscar/templatetags/display_tags.py
"""
from __future__ import unicode_literals

import os
import posixpath
import urllib

from django import template
from django.conf import settings
from django.contrib.staticfiles import finders

from core import get_version

from urllib.parse import urlunparse, urlparse
from django.http import QueryDict


register = template.Library()


@register.simple_tag
def replace_query_param(url, attr, val):
    (scheme, netloc, path, params, query, fragment) = urlparse(url)
    query_dict = QueryDict(query).copy()
    query_dict[attr] = val
    query = query_dict.urlencode()
    return urlunparse((scheme, netloc, path, params, query, fragment))


@register.simple_tag
def staticfile_version(path):
    normalized_path = posixpath.normpath(urllib.parse.unquote(path)).lstrip('/')
    absolute_path = finders.find(normalized_path)
    if not absolute_path and getattr(settings, 'STATIC_ROOT', None):
        absolute_path = os.path.join(settings.STATIC_ROOT, path)
    if absolute_path:
        url = settings.STATIC_URL
        return '%s%s?v=%s' % (url, normalized_path, get_version() )
    return path
