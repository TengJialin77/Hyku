#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import database, date
from common.other import register_appuser


def point_register(nick):

    database.clean_user(nick)  # 删除测试user，保证这个测试user未注册
    register_appuser.register_mobilecode(nick)  # 注册这个测试user
    user_id = database.get_sqldata('accounts', 'nick', nick, 'user_id')  # 将新注册的user的user_id查询出来
    print user_id

    cur1 = database.msql()
    point_active = cur1.get("select * from point where user_id = '%s'" % user_id)['active']
    point_frozen = cur1.get("select * from point where user_id = '%s'" % user_id)['frozen']

    today_point_total = cur1.get("select * from today_point where user_id = '%s' and type = 'total'" % user_id)['point']
    today_point_gift = cur1.get("select * from today_point where user_id = '%s' and type = 'gift'" % user_id)['point']
    today_point_guess = cur1.get("select * from today_point where user_id = '%s' and type = 'guess'" % user_id)
    today_point_invite = cur1.get("select * from today_point where user_id = '%s' and type = 'invite'" % user_id)
    today_point_market = cur1.get("select * from today_point where user_id = '%s' and type = 'market'" % user_id)
    today_point_duel = cur1.get("select * from today_point where user_id = '%s' and type = 'duel'" % user_id)
    today_point_ugc_like = cur1.get("select * from today_point where user_id = '%s' and type = 'ugc_like'" % user_id)


    point_breakdown_gift = cur1.get("select * from point_breakdown where user_id = '%s' and source = 'gift'" % user_id)['point']
    point_breakdown_guess = cur1.get("select * from point_breakdown where user_id = '%s' and source = 'guess'" % user_id)
    point_breakdown_invite = cur1.get("select * from point_breakdown where user_id = '%s' and source = 'invite'" % user_id)
    point_breakdown_market = cur1.get("select * from point_breakdown where user_id = '%s' and source = 'market'" % user_id)
    point_breakdown_duel = cur1.get("select * from point_breakdown where user_id = '%s' and source = 'duel'" % user_id)
    point_breakdown_ugc_like = cur1.get("select * from point_breakdown where user_id = '%s' and source = 'ugc_like'" % user_id)

    users_point_history_gift = cur1.get("select * from users_point_history where user_id = '%s' and task_id = 'gift'" % user_id)['points']










    # print database.get_sqldata('point', 'user_id', user_id, 'active')
    # print database.get_sqldata('point', 'user_id', user_id, 'frozen')
    #
    # assert database.get_sqldata('point', 'user_id', user_id, 'active') == 100
    # assert database.get_sqldata('point', 'user_id', user_id, 'frozen') == 0



point_register('86-13458650253')

    # today_point_guess = cur1.get("select * from today_point where user_id = '%s' and type = 'guess'" % user_id)
    # today_point_invite = cur1.get("select * from today_point where user_id = '%s' and type = 'invite'" % user_id)
    # today_point_market = cur1.get("select * from today_point where user_id = '%s' and type = 'market'" % user_id)
    # today_point_duel = cur1.get("select * from today_point where user_id = '%s' and type = 'duel'" % user_id)
    # today_point_ugc_like = cur1.get("select * from today_point where user_id = '%s' and type = 'ugc_like'" % user_id)

    # point_breakdown_guess = cur1.get("select * from point_breakdown where user_id = '%s' and source = 'guess'" % user_id)
    # point_breakdown_invite = cur1.get("select * from point_breakdown where user_id = '%s' and source = 'invite'" % user_id)
    # point_breakdown_market = cur1.get("select * from point_breakdown where user_id = '%s' and source = 'market'" % user_id)
    # point_breakdown_duel = cur1.get("select * from point_breakdown where user_id = '%s' and source = 'duel'" % user_id)
    # point_breakdown_ugc_like = cur1.get("select * from point_breakdown where user_id = '%s' and source = 'ugc_like'" % user_id)
