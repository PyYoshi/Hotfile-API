#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Hotfile-api
# Copyright 2011 Yoshihiro Misawa
# See LICENSE for details.

from Hotfile.error import HotfileError

class Utils(object):

    @classmethod
    def conv2utf8(cls, arg):
        # written by Michael Norton (http://docondev.blogspot.com/)
        if isinstance(arg, unicode):
            arg = arg.encode('utf-8')
        elif not isinstance(arg, str):
            arg = str(arg)
        return arg

    @classmethod
    def parse_query(cls, query):
        result = {}
        if query:
            name_values = query.split(u'&')
            for name_value in name_values:
                index = name_value.find(u'=')
                if index == -1:
                    name = name_value
                    value = None
                else:
                    name = name_value[:index]
                    value = name_value[index+1:]
                result[name] = result.get(name, []) + [value]
        return result