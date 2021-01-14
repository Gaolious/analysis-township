# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

import pytz
from django import template

register = template.Library()


@register.filter
def split(value, separator=" "):
    return value.split(separator)


@register.filter
def time2datetime(value):
    return datetime.fromtimestamp(value, pytz.timezone('Asia/Seoul'))
