#!/usr/bin/env python
# -*- coding: utf-8 -*-

import myyaml
import requests

def register_mobilecode(mobile):
    url = myyaml.config['domain_app'] + myyaml.api['login_app']
    data = {
        'code': myyaml.config['app_mobilecode'],
        'type': 'mobile_code',
        'mobile': mobile,
        'mob_key': myyaml.config['app_mobkey']
    }
    r = requests.post(url, json=data)
    assert r.status_code == 200
