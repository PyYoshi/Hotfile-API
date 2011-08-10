#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Hotfile-api
# Copyright 2011 Yoshihiro Misawa
# See LICENSE for details.
# Based tweepy. Thanks Joshua Roesslein.

from Hotfile.error import HotfileError
from Hotfile.models import ModelFactory

class ModelParser(object):

    def __init__(self):
        self.model_factory = ModelFactory

    def parse_error(self,  content):
        pass

    def paser(self, method, content):
        model = getattr(self.model_factory, method.parse_type)
        result = model.parse(method, content)
        return result
  