#!/usr/bin/env python
# -*- coding: utf-8 -*-


import myyaml
import random
from common import image, session


def create_ugcpost(content=None, imagename=None, tag=None):
    url = myyaml.config['domain_app'] + myyaml.api['ugc_post']

    if imagename:
        name = imagename
    else:
        name = None

    if content:
        post_content = content
    else:
        post_content = u'我的post %s' % random.randint(0, 100)

    if tag:
        post_tag = tag
    else:
        post_tag = 'tag'

    data = {
        'content': post_content,
        'resources': [
            {
                'url': image.upload_image_post(name),
                'type': 'image',
                'meta': {'height': 200, 'width': 300}
            }
        ],
        'tags': [post_tag]
    }

    s = session.app_session()
    r = s.post(url, json=data)
    assert r.status_code == 200

    print u'创建post成功'

# for i in range(0,23):
#     create_ugcpost(content=str(i), tag='tag002')



#create_ugcpost(imagename='ugc_100x490.jpg')