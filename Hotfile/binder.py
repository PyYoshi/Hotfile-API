#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Hotfile-api
# Copyright 2011 Yoshihiro Misawa
# See LICENSE for details.

from Hotfile.error import HotfileError
from Hotfile.parser import ModelParser
from Hotfile.utils import Utils
from Hotfile.MultipartPostHandler import MultipartPostHandler
import urllib
import urllib2
import cookielib
import time

class Binder(object):

    def __init__(self, **config):
        self.api = config.get('api', None)
        self.action = config.get('action', None)
        self.parse_type = config.get('parse_type', None)
        self.return_keys = config.get('return_keys', None)
        self.login = config.get('login', False)
        self.premium = config.get('premium', False)
        self.format = config.get('format', False)
        self.params = {}
        self.build_params(config.get('options', None))

        if self.login:
            if not self.api.username and not self.api.password_md5dig:
                raise HotfileError('This api is required username and passwd.')
            if self.api.username and self.api.password_md5dig:
                self.build_params({'username':self.api.username})
                self.build_params({'passwordmd5dig':self.api.password_md5dig})
                self.build_params({'digest':self.api.dig})

        if self.format:
            self.build_params(self.api.set_format)

    def build_params(self, options):
        if options is not None:
            for k, arg in options.items():
                if arg == None:
                    continue
                if k in self.params:
                    raise HotfileError('Multiple valus for parameter %s supplied!' % k)
                if isinstance(arg, list):
                    _list = []
                    for v in arg:
                        _list.append(Utils.conv2utf8(v))
                    self.params[k] = _list
                else:
                    self.params[k] = Utils.conv2utf8(arg)

    def build_query(self, params):
        m = 0
        query = ''
        for k,v in params.items():
            if isinstance(v, list):
                line = k + '='
                i = 0
                for l in v:
                    if i == 0:
                        line += urllib.quote(l)
                        i +=1
                    else:
                        line += ',' + urllib.quote(l)
            else:
                line = k + '=' + urllib.quote(v)
            if m == 0:
                query += line
                m += 1
            else:
                query += '&' + line
        return query

    def chkPremium(self):
        pass

    def _execute(self):
        # API URLの作成
        url = 'http://' + self.api.api_host + '/?action=' + self.action + '&' + self.build_query(self.params)
        print url
        # APIからデータを受け取る
        data = urllib2.urlopen(url)
        status = data.code
        msg = data.msg
        content = data.read()
        # パーサ準備
        parser = ModelParser()
        # HTTPエラー処理
        if status != 200:
            if status != 201:
                try:
                    err_msg = 'Server error message: %s Content: %s' % msg, content
                except Exception:
                    err_msg = "Hotfile's API error response: status code = %s " % status
                raise HotfileError(err_msg, data)
        # パーサへデータを受け渡し
        result = parser.paser(self, content)
        return result


class Binder4Web(object):
    def __init__(self, **config):
        self.api = config.get('api', None)
        self.web_path = config.get('web_path', None)
        self.file_path = config.get('file_path', None)
        self.cookie = config.get('cookie', None)
        self.login = config.get('login', False)
        self.payload = config.get('payload', {})
        self.parse_type = config.get('parse_type', None)
        self.retry = config.get('retry', 10)

    def _execute(self):
        opener = None
        headers = [
                ('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.15 Safari/535.1'),
                ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                ('Accept-Language', 'en-us;q=0.7,en;q=0.3'),
                ('Accept-Encoding', 'gzip, deflate'),
                ('Accept-Charset', 'utf-8;q=0.7,*;q=0.7'),
                ('Referer', 'http://hotfile.com/')
            ]

        if self.login:
            login_url = 'http://' + self.api.host + '/login.php'
            login_payload = urllib.urlencode({'returnto':'/', 'user':self.api.username, 'pass':self.api.passwd})
            login_cj = cookielib.LWPCookieJar()
            opener = urllib2.build_opener(
                urllib2.HTTPCookieProcessor(login_cj),
                MultipartPostHandler
            )
            urllib2.install_opener(opener)
            opener.addheaders = headers
            self.cookie = login_cj

            retry = self.retry
            while(retry > 0):
                try:
                    opener.open(login_url, login_payload)
                    break
                except:
                    time.sleep(5)
                retry -= 1

        if not opener:
            if self.cookie:
                opener = urllib2.build_opener(
                    urllib2.HTTPCookieProcessor(self.cookie),
                    MultipartPostHandler
                )
            else:
                opener = urllib2.build_opener()
            opener.addheaders = headers

        url = 'http://' + self.api.host + '/' + self.web_path
        payload = urllib.urlencode(self.payload)
        retry = self.retry
        while(retry > 0):
            try:
                data = opener.open(url, payload)
                content = data.read()
                status = data.code
                msg = data.msg
                if status != 200:
                    if status != 201:
                        try:
                            err_msg = 'Server error message: %s Content: %s' % msg, content
                        except Exception:
                            err_msg = "Hotfile's API error response: status code = %s " % status
                        raise HotfileError(err_msg, data)

                break
            except Exception:
                time.sleep(5)
            retry -= 1
            
        parser = ModelParser()
        result = parser.paser(self, content)
        return result








