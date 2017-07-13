#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import myyaml
import pytest
from Common.excel import get_case


myexcel = get_case('app.xls', 'login')
data = myexcel.get_excel()

parameter_value1 = [(data[0]['account'], data[0]['password'], data[0]['code'])]
parameter_value2 = []
for i in data[1:]:
    a = (str(i['account']), str(i['password']), int(i['code']), i['body_code'])
    parameter_value2.append(a)


@pytest.mark.parametrize('account,password,code', parameter_value1)  # param方法，将account,password,code做成参数，供下方函数使用，用这个方法可以跳过没有通过的脚本继续执行，且更好的查看到哪里错误了
def test_login_success(account,password,code):
    url = myyaml.config['domain_app'] + myyaml.api['login_app']
    data = {
            'code': password,
            'type': 'mobile_password',
            'mobile': account
            }
    s = requests.post(url, json=data)
    assert s.status_code == int(code)


@pytest.mark.parametrize('account,password,code,body_code', parameter_value2)
def test_login_fail(account,password,code,body_code):
    url = myyaml.config['domain_app'] + myyaml.api['login_app']
    data = {
            'code': password,
            'type': 'mobile_password',
            'mobile': account
            }
    s = requests.post(url, json=data)
    assert s.status_code == int(code)
    assert s.json()['error'] == int(body_code)
