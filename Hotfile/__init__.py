#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Hotfile-api
# Copyright 2011 Yoshihiro Misawa
# See LICENSE for details.

"""
Hotfile API Library

Version:
ex) Version 1.2.3 Beta
1: Major version
2: Minor version
3: Revision(bug fix and more...)

History(Learn more https://github.com/PyYoshi/ ):
0.1.0 Pre-Alpha(2011.05.17): Release library.

TODO:
# API-Binder:エラーリトライ実装


Support APIs:
Learn api.py
"""

__vesion__ = '0.1.0'
__author__ = 'Yoshihiro Misawa'
__license__ = 'MIT License'

from Hotfile.error import HotfileError
from Hotfile.api import API
from Hotfile.binder import Binder
from Hotfile.models import Raw
from Hotfile.utils import Utils

# Global, unauthenticated instance of API
api = API()

