#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import session
import myyaml


def review(type, id):  # 提交审核并审核通过
    '''
    :param type: program，episode，info, duel_topic，article
    :param id: 对应type的id
    :return:
    '''

    if type == 'article':
        url_update = myyaml.config['domain_console'] + myyaml.api['review_update_article'].format(article_id=id)
        url_approval = myyaml.config['domain_console'] + myyaml.api['review_approval_article'].format(article_id=id)
    else:
        url_update = myyaml.config['domain_console'] + myyaml.api['review_update_%s' % type].format(id=id)
        url_approval = myyaml.config['domain_console'] + myyaml.api['review_approval_%s' % type].format(id=id)

    s = session.console_session()
    r1 = s.post(url_update)  # 提交审核
    r2 = s.post(url_approval)  # 审核通过
    print r1.status_code
    print r2.status_code
    assert r1.status_code == 200
    assert r2.status_code == 200

#review('program', '58f5b08f64ad611d0648f0ae')

