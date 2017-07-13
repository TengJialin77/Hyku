#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time

import myyaml
from common import image, session
from common.Create import review, channel, id


def create_topic(name=None):

    '''
    :param name: topic名字
    :return:
    '''

    url = myyaml.config['domain_console'] + myyaml.api['topic']
    topic_id = id.create_id('topic')
    small_log_path = image.upload_image_console()
    large_logo_path = image.upload_image_console()
    bg_pic_path = image.upload_image_console()

    if name:
        topic_name = name
    else:
        topic_name = 'MyTopic%s' % random.randint(0, 100)

    data = {'id': topic_id,
            'small_logo': small_log_path,
            'large_logo': large_logo_path,
            'bg_pic': bg_pic_path,
            'description': topic_name
            }

    s = session.console_session()
    r = s.post(url, json=data)
    assert r.status_code == 200

    review.review('topic', topic_id)
    print u'创建主题 %s 成功，id为 %s' % (topic_name, topic_id)

    return topic_id


def create_template(myid, n=None, name=None):

    '''
    :param id: topic_id
    :param n: 过期分钟数
    :return:
    '''
    url = myyaml.config['domain_console'] + myyaml.api['template']

    if myid:
        topic_id = myid
    else:
        topic_id = create_topic()

    if n:
        minute = int(n)
    else:
        minute = 1

    if name:
        description = name
    else:
        description = 'template %s : ' % random.randint(0, 100) + u'女主会和男主在一起吗？'+'('+'%d分钟过期' % minute +')'

    template_id = id.create_id('template')
    channel_id = channel.get_channel_id()

    data = {'id': template_id,
            'topic_id': topic_id,
            'description': description,
            'deadline': long(time.time()*1000 + 60000*minute),
            'channel_id': channel_id,
            'bg_pic': image.upload_image_console(),
            'answers': [
                {
                    'name': u'会',
                    'description': u'女主会和男主在一起',
                    'icon': image.upload_image_console()
                },
                {
                    'name': u'不会',
                    'description': u'女主不会和男主在一起',
                    'icon': image.upload_image_console()
                }
              ],
            'cost': {
                'creator_min_cost': long(1),
                'competitor_min_cost': long(1),
                'competitor_max_cost': long(100),

            }
            }

    s = session.console_session()
    r = s.post(url, json=data)
    assert r.status_code == 200
    review.review('template', template_id)

    print u'创建template %s 成功' % template_id

    return template_id

