#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import myyaml


def console_session():
    url = myyaml.config['domain_console'] + myyaml.api['login_console']
    data = {'account': myyaml.config['console_account'],
            'password': myyaml.config['console_password']
            }
    s = requests.Session()
    r = s.post(url, json=data)
    assert r.status_code == 200
    return s


def merchant_session():
    url = myyaml.config['domain_merchant'] + myyaml.api['login_merchant']
    data = {
        'account': myyaml.config['merchant_account'],
        'password': myyaml.config['merchant_password']
    }
    s = requests.Session()
    r = s.post(url, json=data)
    assert r.status_code == 200
    return s


def app_session():
    url = myyaml.config['domain_app'] + myyaml.api['login_app']
    data = {
        'code': myyaml.config['app_password'],
        'type': 'mobile_password',
        'mobile': myyaml.config['app_account']
    }
    s = requests.Session()
    r = s.post(url, json=data)
    assert r.status_code == 200
    body = r.json()
    s.headers.update({'session': body['session'],
                      'username': body['username']})
    return s
