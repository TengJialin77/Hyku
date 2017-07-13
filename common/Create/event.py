#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time

import myyaml
from common import session, image
from common.Create import review, id


def create_event(start=None, end=None, name=None, type=None, custom=None, imagename=None):

    url = myyaml.config['domain_console'] + myyaml.api['event']

    event_id = id.create_id('event')

    if image:
        event_path = image.upload_image_console()
    else:
        event_path = image.upload_image_console()

    if name:
        event_name = name
    else:
        event_name = 'event %s' % random.randint(0, 100)

    if start:
        start_time = long(time.time()*1000 + 60000*start)
    else:
        start_time = long(time.time()*1000)  # 没有传开始时间，默认当前立刻开始

    if end:
        end_time = long(time.time()*1000 + 60000*end)
    else:
        end_time = start_time + 60000  # 没有传结束时间，默认1分钟后结束

    if type:
        source_type = type
    else:
        source_type = 'all'

    if custom:
        custom_sources = custom
    else:
        custom_sources = {'duel': 'all',
                          'ugc_like': 'all',
                          'guess': 'all',
                          'invite': 'all',
                          'gift': 'all'
                          }

    data_base = {
        'id': event_id,
        'name': event_name,
        'poster': event_path,
        'start_time': start_time,
        'end_time': end_time,
    }
    data_all = {
        'source_type': 'all'
    }
    data_custom = {
        'source_type': 'custom',
        'custom_sources': custom_sources
    }

    if source_type == 'all':
        data = dict(data_base, **data_all)
    elif source_type == 'custom':
        data = dict(data_base, **data_custom)
    else:
        raise ValueError('invalid source_type')

    s = session.console_session()
    r = s.post(url, json=data)
    assert r.status_code == 200

    review.review('event', event_id)
    print u'创建活动 %s 成功，id为 %s' % (event_name, event_id)

    return event_id



