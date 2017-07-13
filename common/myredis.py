#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import myyaml
from common import database

def myredis():
    re = redis.StrictRedis(host=myyaml.config['redis_host'], port=myyaml.config['redis_port'])
    return re

def set_ugcpost_limitnumber(key,value):
    nickname = myyaml.config['app_account']
    userid = database.get_userdata('nick', 'username', nickname)

    re = myredis()
    print key+userid
    re.set(key+userid, value)

#set_ugcpost('/ugcs/posts:',100)

def clean_redis(key=None):
    re = myredis()
    if key:
        keylist = re.keys(key)
    else:
        keylist = re.keys()
    for i in keylist:
        re.delete(i)
        print u'已清除%s'%i


#clean_redis()
