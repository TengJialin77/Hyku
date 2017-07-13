#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os   # 获取目录需要
import random  # 随机抽取图片名字需要
import requests

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from common import session
import myyaml


def image_local_path(name=None):
    '''
    :param name: 按（1.jpg）格式传入image文件夹下的某个图片名字，不传将在image文件夹下随机选取一张
    :return: 图片本地地址
    '''
    if name:
        image_name = name
    else:
        image_name = str(random.randint(1, 40))+'.jpg'
    common_path = os.path.dirname(os.path.abspath(__file__))  # 去掉文件名((获取当前文件路径，包含文件名))
    path = common_path + '\\image\\' + image_name  # 拼接出image文件夹下的某图片地址
    return path


def upload_image_console(imagename=None):

    url = myyaml.config['domain_console'] + myyaml.api['upload_image_console']
    path = image_local_path(imagename)  # 获取本地图片地址
    image_file = open(path, 'rb')  # 打开本地图片，必须用rb格式

    files = {'image': image_file}

    s = session.console_session()
    r = s.post(url, files=files)
    assert r.status_code == 200
    image_path = r.json()['path']
    return image_path


def upload_image_merchant():
    url = myyaml.config['domain_merchant'] + myyaml.api['upload_image_marchant']
    path = image_local_path()
    image_file = open(path, 'rb')

    files = {'image': image_file}

    r = requests.post(url, files=files)
    assert r.status_code == 200

    image_path = r.json()['path']
    return image_path


def upload_image_post(imagename=None):
    url = myyaml.config['domain_app'] + myyaml.api['upload_image_ugcpost']

    if imagename:
        name = imagename
    else:
        name = str(random.randint(1, 40))+'.jpg'

    data = {
        'files': [
            {'name': name,
             'type': 'image'
             }
        ]
    }

    s = session.app_session()
    r = s.post(url, json=data, headers={'X-ClientVersion': '2.5.5'})
    assert r.status_code == 200
    resp = r.json()['files'][0]
    upload_url = resp['upload_url']
    print upload_url
    fields = resp['fields']

    path = image_local_path(name)
    with open(path, 'rb') as fd:  # 这样用可以用完自动关闭掉这个文件
        r1 = s.post(upload_url, data=fields, files={"file": fd})
    assert r1.status_code == 200
    return resp['access_path']

#upload_image_post()















