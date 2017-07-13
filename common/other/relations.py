#!/usr/bin/env python
# -*- coding: utf-8 -*-

import myyaml
from common import session, database

def friends(usernick):

    url = myyaml.config['domain_app'] + myyaml.api['relations']
    username = database.get_username(usernick)

    data = {
        'target': username,
    }

    s = session.app_session()
    r = s.post(url, json=data)
    assert r.status_code == 200

friends(u'藤藤')




