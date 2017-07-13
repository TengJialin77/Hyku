#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import os


def get_api():
    yaml_path = os.path.dirname(os.path.abspath(__file__)) + '\myapi.yaml'  # Config.yaml文件的地址
    yaml_file = open(yaml_path)   # 打开yaml
    yaml_data = yaml.load(yaml_file)  # 获取yaml具体内容，返回dict列表
    return yaml_data

api = get_api()  # 获取myapi.yaml文件里面的列表，赋值给变量api


def get_config(region):
    yaml_path = os.path.dirname(os.path.abspath(__file__)) + '\myconfig.yaml'  # Config.yaml文件的地址
    yaml_file = open(yaml_path)   # 打开yaml
    yaml_data = yaml.load(yaml_file)  # 获取yaml所有内容，返回dict列表
    return yaml_data[region]

cn_config = get_config("cn")  # 获取myconfig.yaml文件里面的cn下的列表，赋值给变量cn_config
id_config = get_config("id")  # 获取myconfig.yaml文件里面的id下的列表，赋值给变量id_config
config = cn_config  # config默认值


def set_region(newregion):   # 根据传入的region，获取到myconfig.yaml文件里面对应region下的列表，赋值给变量config
    global config
    if newregion == "id":
        config = id_config
    elif newregion == "cn":
        config = cn_config
    else:
        raise ValueError(u'参数传入错误')
    return config
