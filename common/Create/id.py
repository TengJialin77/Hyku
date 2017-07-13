#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import session
import myyaml



def create_id(type):
    '''
    :param type: 分配id的类型,可选值为(program|episode|info|channel|topic|template)
    :return: 返回id
    '''

    url = myyaml.config['domain_console'] + myyaml.api['create_id'].format(type=type)

    data = {'count': 1}

    s = session.console_session()
    r = s.post(url, json=data)

    assert r.status_code == 200

    id = r.json()[0]
    return id

#create_id('program')


#global_create = partial(create_id, myconfig.get("region"))
