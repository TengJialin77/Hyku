#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import session
import random
import myyaml


def create_market_use():

    url = myyaml.config['domain_console'] + myyaml.api['create_merchant_user']

    account = 'test%s' % random.randint(0, 100)
    name = account
    phone = '+86 13458650253'
    password = '111111'

    data = {
        'account': account,
        'name': name,
        'phone': phone,
        'password': password
    }

    s = session.console_session()
    r = s.post(url, json=data)

    assert r.status_code == 200

    print u'创建商户 %s 成功，密码为111111' % account


#myyaml.set_region('cn')
#create_market_use()