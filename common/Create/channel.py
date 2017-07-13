#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

import myyaml
from common.Create import id
from common import session, image


def create_channel():
    url = myyaml.config['domain_console'] + myyaml.api['channel']
    channel_id = id.create_id('channel')
    channel_name = 'Hyku ' + str(random.randint(0, 100))
    channel_icon = image.upload_image_console()  # 调用image.py的image_path()，随机上传一张图片并得到图片在服务器的地址

    data = {'id': channel_id,
            'name': channel_name,
            'icon': channel_icon
            }

    s = session.console_session()
    r = s.post(url, json=data)
    assert r.status_code == 200


def get_channel_id():
    url = myyaml.config['domain_console'] + myyaml.api['channel']
    data = {'with_image': 'false'}
    s = session.console_session()
    r = s.get(url, data=data)
    assert r.status_code

    channel = r.json()
    if len(channel) == 0:
        channel1_id = create_channel()
    else:
        channel1 = channel[0]
        channel1_id = channel1['id']

    return channel1_id









