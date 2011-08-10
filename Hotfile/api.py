#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Hotfile-api
# Copyright 2011 Yoshihiro Misawa
# See LICENSE for details.

from Hotfile.error import HotfileError
from Hotfile.binder import Binder, Binder4Web

import md5
import ftplib
from datetime import date
import os

class API(object):
    """Hotfile API"""
    # http://api.hotfile.com/

    def __init__(self, username=None, passwd=None):
        self.api_host = 'api.hotfile.com'
        self.ftp_host = 'ftp.hotfile.com'
        self.host = 'hotfile.com'
        self.set_format = {
            'fieldseparator' : ',',
            'lineseparator' : '\n',
            'fields':['status','id','name','size','md5']
        }
        self.username = username
        self.passwd = passwd
        if username and passwd:
            m1 = md5.new()
            m1.update(passwd)
            passwd_md5 = m1.hexdigest()
            self.dig = self._getdigest()
            m2 = md5.new()
            m2.update(passwd_md5 + self.dig)
            self.password_md5dig = m2.hexdigest()

    ###### 内部実装 ######

    def _getdigest(self):
        binder = Binder(
            api = self,
            action = 'getdigest',
            parse_type = 'raw',
            options = None,
            format = False,
            login = False,
            premium = False
        )
        return binder._execute()

    def _getuserinfo(self):
        binder = Binder(
            api = self,
            action = 'getuserinfo',
            parse_type = 'qstr',
            options = None,
            format = False,
            login = True,
            premium = False
        )
        return binder._execute()

    def _checklinks(self, links=None, ids=None, keys=None):
        # 引数チェック: linksまたはidsとkeysを引数としていない場合エラーを吐く
        if not links:
            if not ids or not keys:
                raise HotfileError('Required links or ids and keys.')

        # 引数の型チェック
        if links and not isinstance(links, list):
            raise HotfileError('links is invalid list type. ex.) links = ["http://hotfile.com/dl/(id)/(key)/(file name).html",]')
        if ids and not isinstance(ids, list):
            raise HotfileError('ids is invalid list type. ex.) ids = ["123456789",]')
        if keys and not isinstance(keys, list):
            raise HotfileError('keys is invalid list type. ex.) keys = ["abcdefghi",]')
        binder = Binder(
            api = self,
            action = 'checklinks',
            parse_type='fields',
            options = {
                'links':links,
                'ids':ids,
                'keys':keys,
            },
            format = True,
            login = False,
            premium = False
        )
        return binder._execute()

    def _getdirectdownloadlink(self, link, alllinks=None):
        # 未実装
        # return:
        # 型チェック
        if not isinstance(link, str):
            raise HotfileError('link is invalid str type. ex.) ids = ""')
        if alllinks and not isinstance(alllinks, list):
            raise HotfileError('alllinks is invalid list type. ex.) alllinks = ["",""]')
        binder = Binder(
            api = self,
            action = 'getdirectdownloadlink',
            parse_type='Raw',
            options = {
                'link':link,
                'alllinks':alllinks
            },
            format = False,
            login = True,
            premium = True
        )
        return binder._execute()

    def _getuploadserver(self, count=None):
        # 型チェック
        if count and not isinstance(count, int):
            raise HotfileError('count is invalid int type. ex.) count = ["",""]')
        # 最大値チェック
        if count and not count < 0 and count > 5:
            raise  HotfileError('count is maximum 5.')
        binder = Binder(
            api = self,
            action = 'getuploadserver',
            parse_type='lf',
            options = {
                'count':count
            },
            format = False,
            login = False,
            premium = False
        )
        return binder._execute()

    def _createfolder(self, name, parentfolderid=None, parentfolder=None):
        # return: folderid,folderhash,path
        # 型チェック
        if not isinstance(name, str):
            raise HotfileError('name is invalid str type. ex.) name = ""')
        if parentfolderid and not isinstance(parentfolderid, str):
            raise HotfileError('parentfolderid is invalid str type. ex.) parentfolderid = ""')
        if parentfolder and not isinstance(parentfolder, str):
            raise HotfileError('parentfolder is invalid str type. ex.) parentfolder = ""')
        #
        binder = Binder(
            api = self,
            action = 'createfolder',
            parse_type='comma',
            options = {
                'name':name,
                'parentfolderid':parentfolderid,
                'parentfolder':parentfolder
            },
            format = False,
            return_keys = ['folderid', 'folderhash', 'path'],
            login = True,
            premium = False
        )
        return binder._execute()

    def _deletefolder(self, name=None, parentfolderid=None, parentfolder=None):
        # return: "OK" or error message(".folder does not exists").
        # 型チェック
        if name and not isinstance(name, str):
            raise HotfileError('name is invalid str type. ex.) name = ""')
        if parentfolderid and not isinstance(parentfolderid, str):
            raise HotfileError('parentfolderid is invalid str type. ex.) parentfolderid = ""')
        if parentfolder and not isinstance(parentfolder, str):
            raise HotfileError('parentfolder is invalid str type. ex.) parentfolder = ""')
        #
        binder = Binder(
            api = self,
            action = 'deletefolder',
            parse_type='raw',
            options = {
                'name':name,
                'parentfolderid':parentfolderid,
                'parentfolder':parentfolder
            },
            format = False,
            login = True,
            premium = False
        )
        return binder._execute()

    def _renamefolder(self, name=None, parentfolderid=None, parentfolder=None, folderid=None, newname=None, newparentfolderid=None, newparentfolder=None):
        # return:
        # どのようなパラメータ入れても、APIエラーが発生するため未実装。
        # 型チェック
        if name and not isinstance(name, str):
            raise HotfileError('name is invalid str type. ex.) name = ""')
        if parentfolderid and not isinstance(parentfolderid, str):
            raise HotfileError('parentfolderid is invalid str type. ex.) parentfolderid = ""')
        if parentfolder and not isinstance(parentfolder, str):
            raise HotfileError('parentfolder is invalid str type. ex.) parentfolder = ""')
        if folderid and not isinstance(folderid, str):
            raise HotfileError('folderid is invalid str type. ex.) folderid = ""')
        if newname and not isinstance(newname, str):
            raise HotfileError('newname is invalid str type. ex.) newname = ""')
        if newparentfolderid and not isinstance(newparentfolderid, str):
            raise HotfileError('newparentfolderid is invalid str type. ex.) newparentfolderid = ""')
        if newparentfolder and not isinstance(newparentfolder, str):
            raise HotfileError('newparentfolder is invalid str type. ex.) newparentfolder = ""')
        #
        binder = Binder(
            api = self,
            action = 'renamefolder',
            parse_type='raw',
            options = {
                'name':name,
                'parentfolderid':parentfolderid,
                'parentfolder':parentfolder,
                'folderid':folderid,
                'newname':newname,
                'newparentfolderid':newparentfolderid,
                'newparentfolder':newparentfolder
            },
            format = False,
            login = True,
            premium = False
        )
        return binder._execute()

    def _deletefile(self, fileid=None, name=None, folder=None, folderid=None):
        # return: OK or error message. (".file not found")
        # 型チェック
        if fileid and not isinstance(fileid, str):
            raise HotfileError('fileid is invalid str type. ex.) fileid = ""')
        if name and not isinstance(name, str):
            raise HotfileError('name is invalid str type. ex.) name = ""')
        if folder and not isinstance(folder, str):
            raise HotfileError('folder is invalid str type. ex.) folder = ""')
        if folderid and not isinstance(folderid, str):
            raise HotfileError('folderid is invalid str type. ex.) folderid = ""')
        #
        binder = Binder(
            api = self,
            action = 'deletefile',
            parse_type='raw',
            options = {
                'fileid':fileid,
                'name':name,
                'folder':folder,
                'folderid':folderid
            },
            format = False,
            login = True,
            premium = False
        )
        return binder._execute()

    def _undeletefile(self, fileid=None, name=None, folder=None, folderid=None):
        # return: OK or error message. (".file not found")
        # 型チェック
        if fileid and not isinstance(fileid, str):
            raise HotfileError('fileid is invalid str type. ex.) fileid = ""')
        if name and not isinstance(name, str):
            raise HotfileError('name is invalid str type. ex.) name = ""')
        if folder and not isinstance(folder, str):
            raise HotfileError('folder is invalid str type. ex.) folder = ""')
        if folderid and not isinstance(folderid, str):
            raise HotfileError('folderid is invalid str type. ex.) folderid = ""')
        #
        binder = Binder(
            api = self,
            action = 'undeletefile',
            parse_type='raw',
            options = {
                'fileid':fileid,
                'name':name,
                'folder':folder,
                'folderid':folderid
            },
            format = False,
            login = True,
            premium = False
        )
        return binder._execute()

    def _hotlinkfile(self, fileid=None, hotlink=None, name=None, folder=None, folderid=None):
        # return:
        # プレミアム垢ないので未実装
        # 型チェック
        if fileid and not isinstance(fileid, str):
            raise HotfileError('fileid is invalid str type. ex.) fileid = ""')
        if hotlink and not isinstance(hotlink, int):
            raise HotfileError('hotlink is invalid int type. ex.) hotlink = 0 or 1')
        if name and not isinstance(name, str):
            raise HotfileError('name is invalid str type. ex.) name = ""')
        if folder and not isinstance(folder, str):
            raise HotfileError('folder is invalid str type. ex.) folder = ""')
        if folderid and not isinstance(folderid, str):
            raise HotfileError('folderid is invalid str type. ex.) folderid = ""')
        # on/offチェック
        if not hotlink == 0 or not hotlink == 1:
            raise HotfileError('Invalid value. 0: Disable hotlink. 1: Enable hotlink.')
        #
        binder = Binder(
            api = self,
            action = 'hotlinkfile',
            parse_type='',
            options = {
                'fileid':fileid,
                'hotlink':hotlink,
                'name':name,
                'folder':folder,
                'folderid':folderid
            },
            format = False,
            login = True,
            premium = True
        )
        return binder._execute()

    def _getdirectdownloadlinks(self, links):
        # return:
        # プレミアム垢ないので未実装
        # 型チェック
        if not isinstance(links, list):
            raise HotfileError('links is invalid list type. ex.) links = ["",""]')
        #
        binder = Binder(
            api = self,
            action = 'getdirectdownloadlinks',
            parse_type='raw',
            options = {
                'links':links
            },
            format = False,
            login = True,
            premium = True
        )
        return binder._execute()

    def _sendvalidationcode(self):
        # return: OK/error message
        #
        binder = Binder(
            api = self,
            action = 'sendvalidationcode',
            parse_type='raw',
            options = None,
            format = False,
            login = True,
            premium = False
        )
        return binder._execute()

    def _changepassword(self, password_new ,validationcode):
        # return: OK/error message
        # 型チェック
        if not isinstance(password_new, str):
            raise HotfileError('psasword_new is invalid str type. ex.) psasword_new = ""')
        if not isinstance(validationcode, str):
            raise HotfileError('validationcode is invalid str type. ex.) validationcode = ""')
        #
        binder = Binder(
            api = self,
            action = 'changepassword',
            parse_type='raw',
            options = {
                'password_new':password_new,
                'validationcode':validationcode
            },
            format = False,
            login = True,
            premium = False
        )
        return binder._execute()

    def _getdownloadlinksfrompublicdirectory(self, folder, hash, forcenonprem=None):
        # return:ファイル名|リンクURL\n
        # 型チェック
        if not isinstance(folder, str):
            raise HotfileError('folder is invalid int type. ex.) folder = ""')
        if not isinstance(hash, str):
            raise HotfileError('hash is invalid str type. ex.) hash = ""')
        if forcenonprem and not isinstance(forcenonprem, str):
            raise HotfileError('forcenonprem is invalid str type. ex.) forcenonprem = ""')
        #
        binder = Binder(
            api = self,
            action = 'getdownloadlinksfrompublicdirectory',
            parse_type='raw',
            options = {
                'folder':folder,
                'hash':hash,
                'forcenonprem':forcenonprem
            },
            format = False,
            login = True,
            premium = False
        )
        return binder._execute()

    def _get_dir_file_ftp(self):
        if not self.passwd:
            raise HotfileError('Not set username or password.')
        # これはAPI側で実装されたものではありません。ftp経由でアップロードできるため、そちらを使っています。
        ftp = ftplib.FTP(host=self.ftp_host)
        ftp.login(user=self.username, passwd=self.passwd)
        self.ftp_files = []
        if ftp.pwd() == '/':
            self.ftp_pwd = ''
        else:
            self.ftp_pwd = ftp.pwd()

        ftp.retrlines('LIST', self.__ret_all_file_detail)

        for file_ in self.ftp_files:
            if file_['permission'][0] == 'd':
                self.ftp_pwd = file_['path']
                ftp.cwd(self.ftp_pwd)
                ftp.retrlines('LIST', self.__ret_all_file_detail)
                
        ftp.quit()
        return self.ftp_files

    def __ret_all_file_detail(self, line):
        tmp = line.split(' ')
        name = tmp[-1]
        permission = tmp[0]
        user = tmp[6]
        year = tmp[-2]
        if tmp[-5] == '':
            mon = tmp[-6]
            day = tmp[-4]
        else:
            mon = tmp[-5]
            day = tmp[-4]

        # Directoryの時
        if permission[0] == 'd':
            size = None
        # Fileの時
        elif permission[0] == '-':
            size = tmp[12]
        # それ以外の時
        else:
            raise HotfileError('Unknown file type. %s' % line)

        mon_list = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
        date_ = date(int(year), mon_list[mon], int(day))


        file_ = {
            'permission':permission,
            'user':user,
            'date':date_,
            'fsize':size,
            'name':name,
            'path': self.ftp_pwd + '/' + name
        }

        if name == '.':
            pass
        elif name == '..':
            pass
        else:
            self.ftp_files.append(file_)

    def _upload_ftp(self, filename, upload_dirpath='/'):
        if not self.passwd:
            raise HotfileError('Not set username or password.')
        try:
            ftp = ftplib.FTP(host=self.ftp_host)
        except Exception, e:
            raise HotfileError('Could not connect to the ftp server.', e)
        try:
            ftp.login(user=self.username, passwd=self.passwd)
        except Exception, e:
            raise HotfileError('Could not login to the ftp server.', e)

        try:
            fp = open(filename, "rb")
            fpname = os.path.basename(filename)
            if upload_dirpath == '/':
                upload_path = '/' + fpname
            else:
                upload_path = upload_dirpath+'/'+fpname
                # ディレクトリがあるかのチェック。なければ作成。
                for p in upload_dirpath.split('/')[1:]:
                    try:
                        ftp.cwd(p)
                    except Exception, e:
                        print 'Create %s directory.' % p
                        ftp.mkd(p)
                        ftp.cwd(p)
        except Exception, e:
            raise HotfileError('Invalid file path.', e)
        
        try:
            ftp.storbinary('STOR '+upload_path, fp)
            ftp.close()
            fp.close()
        except Exception, e:
            raise HotfileError('Invalid file path.', e)

        try:
            return self._get_dl_link_from_path(upload_path).link
        except Exception, e:
            raise HotfileError('Could not get download link.', e)
        
    def _get_resouces(self, web_path, cookie=None):
        binder = Binder4Web(
            api = self,
            web_path = web_path,
            cookie = cookie,
            parse_type = 'raw'
        )
        return binder._execute()

    def _get_myfiles_links_web(self):
        binder = Binder4Web(
            api = self,
            login = True,
            web_path = 'myfiles.html',
            parse_type = 'myfiles'
        )
        return binder._execute()

    def _get_myfolder_links(self):
        binder = Binder4Web(
            api = self,
            login = True,
            web_path = 'myfolders.html',
            parse_type = 'myfolders'
        )
        return binder._execute()

    def _get_dl_link_from_path(self, file_path):
        binder = Binder4Web(
            api = self,
            login = True,
            file_path = file_path,
            web_path = 'myfolders.html',
            parse_type = 'myfile'
        )
        return binder._execute()

    ###### 外部実装 ######
