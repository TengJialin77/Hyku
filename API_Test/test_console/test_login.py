#!/usr/bin/env python
# -*- coding: utf-8 -*-

import myyaml
import requests
import pytest
from API_Test.excel import excel


myexcel = excel('console.xls', 'login')
data = myexcel.get_excel()

parameter_value = []
for i in data:
    a = (str(i['account']), str(i['password']), int(i['code']))
    parameter_value.append(a)

@pytest.mark.parametrize('account,password,code', parameter_value)  # param方法，将account,password,code做成参数，供下方函数使用，用这个方法可以跳过没有通过的脚本继续执行，且更好的查看到哪里错误了
def test_login(account,password,code):
    url = myyaml.config['domain_console'] + myyaml.api['login_console']
    data = {
            'account': account,
            'password': password
            }
    s = requests.post(url, json=data)
    assert s.status_code == code