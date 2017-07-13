#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import random
import string
import torndb
from uuid import uuid5, NAMESPACE_X500

from pymongo import MongoClient
from xpinyin import Pinyin
from pymongo.errors import DuplicateKeyError

mysql_client = torndb.Connection("db-mysql.dev-cn.internal.hyku.org:3306", "dev_cn_db_console", "root", "pabb")
collection_account = MongoClient("db-main.dev-cn.internal.hyku.org", 27017)["hrmes_server"]["account"]


class Random(object):
    _population = string.ascii_letters + string.digits

    @staticmethod
    def digit(n):
        if n > 0:
            return ''.join(random.choice(string.digits) for i in range(n))
        return ''

    @staticmethod
    def alphanumeric(n):
        if n > 0:
            return ''.join(random.choice(Random._population) for i in range(n))
        return ''


class InitAccount(object):
    @classmethod
    def register(cls, mobile, password, zone):
        """
        if you want to change zone, please check the mongodb host and mysql host.
        """
        doc = collection_account.find_one({"mobile": mobile})
        if doc is None:
            try:
                salt = Random.alphanumeric(256)
                p = Pinyin()
                nick = mobile
                # return json info
                new_user_info = {'username': ''.join([zone, Random.digit(10)]),
                                 'salt': salt,
                                 'device': "Transformer 101",
                                 'device_model': "Transformer",
                                 'ua': "Hyku mock",
                                 'device_type': "ios",
                                 'nick': nick,
                                 'pinyin': p.get_pinyin(nick, u'').lower(),
                                 'initials': p.get_initials(nick, u'').lower(),
                                 'profile_image': "/ugc/profile/avatar.jpg",
                                 'profile_banner': None,
                                 'post_count': 0,
                                 'email': None,
                                 # feature 1.6.1
                                 'mobile': mobile,
                                 'invite': str(uuid5(NAMESPACE_X500, mobile))[-6:],
                                 'invited_by': "",
                                 'has_password': True,  # password exists :1 ,not :0
                                 "password": hashlib.sha256(
                                     password.encode('UTF-8') + salt.encode('UTF-8')).hexdigest(),
                                 'birthday': None,
                                 'gender': 3,
                                 'location': None,
                                 'signature': None,
                                 'weibo': None,
                                 'weixin': None,
                                 'facebook': None,
                                 'twitter': None,
                                 'subscribed_threads': []
                                 }
                collection_account.insert_one(new_user_info)
                mysql_client.execute("INSERT INTO point (user_id,active,frozen) VALUE (%s,%s,%s)",
                                     new_user_info["username"], 500, 0)
                print "register success for %s,<%s>" % (mobile, new_user_info["username"])
            except DuplicateKeyError as e:
                print "duplicated", e

        print "done"


if __name__ == "__main__":
    for i in range(30,60):
     account = '86-123456789%d' %i
     InitAccount.register(account, '111111', 'zh')




