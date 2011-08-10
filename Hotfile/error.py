#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Hotfile-api
# Copyright 2011 Yoshihiro Misawa
# See LICENSE for details.
# Based tweepy. Thanks Joshua Roesslein.

class HotfileError(Exception):
    """Pytumb exception"""

    def __init__(self, reason, response=None):
        self.reason = str(reason)
        self.response = response
        #print self.response

    def __str__(self):
        return self.reason