#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Hotfile-api
# Copyright 2011 Yoshihiro Misawa
# See LICENSE for details.

from Hotfile.error import HotfileError
from Hotfile.utils import Utils
from BeautifulSoup import BeautifulSoup as BS
import re

# プレコンパイル
preDLLink = re.compile('(http|https):\/\/hotfile\.com\/dl\/([a-zA-Z0-9]*)\/([a-zA-Z0-9]*)\/(.+)\.html')
preFolderLink = re.compile('(http|https):\/\/hotfile\.com\/list\/([a-zA-Z0-9]*)\/([a-zA-Z0-9]*)')
preMyFilesLink = re.compile(r'^/myfiles.html\?d\=(\d+)\-(\d+)-(\d+)$')
preURL = re.compile(r'(http://[A-Za-z0-9\'~+\-=_.,/%\?!;:@#\*&\(\)]+)')
preFilename = re.compile("filenames\[(\d+)\].\=.\'(.+)\s\'\;")


class Model(object):
    def __init__(self, api=None):
        self._api = api

        def __getstate__(self):
            pickle = dict(self.__dict__)
            try:
                del pickle['_api']
            except KeyError:
                pass
            return pickle

    @classmethod
    def parse(cls, api, content):
        raise NotImplementedError

class Raw(Model):
    @classmethod
    def parse(cls, api, content):
        return content

class QueryString(Model):
    @classmethod
    def parse(cls, api, content):
        dict = Utils.parse_query(content)
        qstr = cls(api)
        for k, v in dict.items():
            setattr(qstr, k, v)
        return qstr

class Fields(Model):
    @classmethod
    def parse(cls, api, content):
        fieldseparator_format = api.api.set_format['fieldseparator']
        lineseparator_format =api.api.set_format['lineseparator']
        fields_format = api.api.set_format['fields']
        lines = content.split(lineseparator_format)[:-1]
        fields = cls(api)
        files = []
        for line in lines:
            line_values = line.split(fieldseparator_format)
            i = 0
            file = {}
            for v in line_values:
                file[fields_format[i]] = v
                i += 1
            files.append(file)
        setattr(fields, 'fields', files)
        return fields

class Lf(Model):
    @classmethod
    def parse(cls, api, content):
        lf = cls(api)
        setattr(lf, 'lf', content.split('\n')[:-1])
        return  lf

class Commma(Model):
    @classmethod
    def parse(cls, api, content):
        return_keys = api.return_keys
        dic = dict(zip(return_keys,content.split(',')))
        commma = cls(api)
        setattr(commma, 'commma', dic)
        return commma

class MyFiles(Model):
    @classmethod
    def parse(cls, api, content):
        # id "loginFormMenu"が存在する場合はログインされていない。
        # class "my_files"内に存在。
        links = []
        files = cls(api)
        soup = BS(content)
        for l in soup.findAll('script'):
            m = preDLLink.search(l.text)
            if m:
                links.append(m.group())

        for s in soup.findAll('a'):
            if preMyFilesLink.match(s.get('href', None)):
                soup2 = BS(api.api._get_resouces(s.get('href', None)[1:], api.cookie))
                for l2 in soup2.findAll('script'):
                    m2 = preDLLink.search(l2.text)
                    if m2:
                        links.append(m2.group())
        setattr(files, 'myfolders', links)
        return files

                
class MyFolders(Model):
    @classmethod
    def parse(cls, api, content):
        myfolders = cls(api)
        links = []
        soup = BS(content)
        dirs_path = {}
        for t in soup.findAll('tr',attrs={'id':'copyform'}):
            for s in t.findAll('option'):
                folder_id = s.get('value', None)
                dir_path = s.text
                dirs_path[folder_id] = dir_path
                if folder_id:
                    if folder_id != 'None':
                        web_path = 'myfolders.html?o=' + folder_id
                        soup2 = BS(api.api._get_resouces(web_path, api.cookie))
                        for l in soup2.findAll('script'):
                            m = preFolderLink.search(l.text)
                            if m:
                                links.append(m.group())

        # リストの重複削除
        links = list(set(links))
        folders = []
        for link in links:
            folder = {}
            m2 = preFolderLink.search(link)
            tmp_id = m2.group(2)
            tmp_hash = m2.group(3)
            tmp_path = dirs_path[tmp_id][:-1]
            tmp_name = tmp_path.split('/')[-1]
            folder = {
                'link' : link,
                'folder_id' : tmp_id,
                'folder_hash': tmp_hash,
                'path' : tmp_path,
                'folder_name' : tmp_name
            }
            folders.append(folder)

        setattr(myfolders, 'myfolders', folders)
        return myfolders

class MyFile(Model):
    @classmethod
    def parse(cls, api, content):
        link = cls(api)
        file_name = api.file_path.split('/')[-1]
        path = re.sub('/'+file_name, '', api.file_path)
        soup = BS(content)
        dirs_path = {}
        for t in soup.findAll('tr',attrs={'id':'copyform'}):
            for s in t.findAll('option'):
                folder_id = s.get('value', None)
                dir_path = s.text
                if dir_path != 'None':
                    dirs_path[dir_path[:-1]] = folder_id
        if dirs_path:
            folder_id = dirs_path[path]
            web_path = 'myfolders.html?o=' + folder_id
            soup2 = BS(api.api._get_resouces(web_path, api.cookie))
            for l in soup2.findAll('script'):
                m = preDLLink.search(l.text)
                if m:
                    if m.group(4) == file_name:
                        dl_link = m.group()
                        break

            setattr(link, 'link', dl_link)
            return link



        

            

class ModelFactory(object):
    raw = Raw
    qstr = QueryString
    fields = Fields
    lf = Lf
    comma = Commma
    myfiles = MyFiles
    myfolders = MyFolders
    myfile = MyFile