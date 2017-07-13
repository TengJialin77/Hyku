#!/usr/bin/env python
# -*- coding: utf-8 -*-

import myyaml
import random
from common import session, image
from common.Create import review

def create_article(name=None):
    url = myyaml.config['domain_console'] + myyaml.api['create_article']

    if name:
        article_name = name
    else:
        article_name = 'MyArticle %s' % random.randint(0, 1000)

    data = {
        'title': article_name,
        'image': image.upload_image_console(),
        'content': u'这里是文章内容',
        'share': {
            'title': 'share_title:%s' % article_name,
            'text': 'share_text:%s' % article_name,
            'image': image.upload_image_console('share.jpg')
        }

    }

    s = session.console_session()
    r = s.post(url, json=data)
    assert r.status_code == 200
    article_id = r.json()['id']
    review.review('article', article_id)
    return article_id


def get_articles_id():
    url = myyaml.config['domain_console'] + myyaml.api['get_article']
    s = session.console_session()
    r = s.get(url)

    article = r.json()
    if len(article) == 0:
        article_id = create_article()
    else:
        article_id = article['items'][0]['id']

    return article_id



