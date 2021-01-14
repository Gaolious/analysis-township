# -*- coding: utf-8 -*-
from __future__ import unicode_literals


__all__ = ['get_version', 'get_short_version']

PROD, DEV, ALPHA, BETA = ('p', 'd', 'a', 'b')

###############################################################
YEAR = 2020
MONTH = 3
DAY = 4
PATCH = 1
MODE = DEV
###############################################################


VERSION = (YEAR, MONTH, DAY, PATCH, MODE)


def get_short_version():
    return '%04d.%02d.%02d' % (VERSION[0], VERSION[1], VERSION[2])


def get_version():
    return '%04d.%02d.%02d-%d%s' % (
    VERSION[0], VERSION[1], VERSION[2], VERSION[3], VERSION[4])
