#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo  # 链接mongodb工具
import torndb  # 链接mysql工具

import myyaml
from common import date


def msql():
    conn = torndb.Connection(myyaml.config['mysql_host'], myyaml.config['mysql_database'], myyaml.config['mysql_user'], myyaml.config['mysql_password'])
    return conn


def get_sqldata(table, factor, factor_value, intent):
    '''
    :param table: 查询的表
    :param factor: 查询条件
    :param factor_value: 查询条件的值
    :param intent: 查询目标
    :return:
    '''
    cur1 = msql()
    user = cur1.get("select * from %s where %s = '%s'" % (table, factor,factor_value))
    if user:
        userdata = user[intent]
    else:
        print u'没有找到相关内容'
        userdata = None
    return userdata


def clean_all():
    cur1 = msql()  # 链接mysql数据库
    name = ('account_device_infos',
            'addresses',
            'article_like_action', 'articles', 'article_replies', 'articles_draft',
            'attribute_options','attributes',
            'audit_log',
            'banners', 'banners_draft',
            'brands',
            'categories',
            'channels',
            'cs_group', 'cs_group_admin', 'cs_group_resource',
            'draft_article_info', 'draft_episodes', 'draft_guess_info', 'draft_info', 'draft_product_info', 'draft_program_tags', 'draft_programs', 'draft_text_info', 'draft_vote_info',
            'duel_answer','duel_history_count', 'duel_instance', 'duel_template', 'duel_template_order', 'duel_topic', 'duel_topic_order',
            'episode_user_footprint',
            'event',
            'favorites',
            'feedbacks',
            'followed', 'following', 'friends',
            'guess_choices', 'guess_results',
            'home_review',
            'image_resource',
            'info_like_actions', 'info_replies', 'info_user_datas',
            'lotteries', 'lotteries_draft', 'lottery_orders',
            'market_point_history',
            'merchants',
            'notification', 'notification_unread_count',
            'operator_merchant_map', 'operator_order_memo', 'operators',
            'order_logistics',
            'point', 'point_breakdown', 'point_history',
            'product_order_skus',
            'product_orders',
            'program_point_history',
            'relation_meta', 'released_article_info','released_episodes','released_guess_info','released_info','released_product_info','released_programs','released_text_info','released_vote_info',
            'sku_attribute_map', 'sku_audit_log', 'sku_statistic', 'skus', 'spu_attribute_map', 'spus',
            'stocks', 'stocks_draft',
            'tab_item_groups', 'tab_item_groups_draft', 'tab_items', 'tab_items_draft', 'tabs', 'tabs_draft',
            'tag', 'tag_article', 'tag_article_draft', 'tag_duel', 'tag_program', 'tag_ugc',
            'tbl_account_bind', 'tbl_cookie', 'tbl_user_resource', 'tbl_resource', 'tbl_user_owner', 'tbl_user_profile',
            'thirdparty_infos',
            'today_point',
            'tourney',
            'ugc_like_action', 'ugc_point_history', 'ugc_post', 'ugc_reply', 'ugc_report', 'ugc_report_handle',
            'users_point_history',
            'vote_choices','vote_results',
          )
    for i in name:  # 清空name列表里面的每一个表
        cur1.execute('delete from %s' % i)
    print u'已清空mysql基本表'

    cur1.execute("delete from cs_admin where id not in ('builtin_root')")
    print u'已清空内容后台除root以外的所有账号'

    cur1.execute("delete from accounts where user_id not in ('4881675438')")
    print u'已清空app用户除hyku以外的所有账号'


    d1 = cur1.query('SELECT table_name FROM information_schema.tables WHERE table_name LIKE %s','event\_%')  # 查询获取所有event开头的表名字，赋值给的d1
    for i1 in d1:   # 轮询出每个event开头的表，并删除
        i2 = i1['table_name']
        cur1.execute('drop table %s' % i2)
    print u'已删除mysql数据库中event开头的表'

    d2 = cur1.query('SELECT table_name FROM information_schema.tables WHERE table_name LIKE %s', 'weekly\_%')  # 查询获取所有weekly开头的表名字，赋值给的d2
    if len(d2) == 0:  # 判断是否有weekly开头的表
        print (u'没有weekly开头的表')
    else:
        list_delete = []
        list_clean = []
        for i3 in d2:
            table_name = i3['table_name']
            if table_name < 'weekly_%s_point' % date.get_date(1):  # 判断这个表是否已经是历史表，不是本周还在用的表
                list_delete.append(table_name)  # 将历史表加入list_delete列表，下方直接删除整个表
            else:
                list_clean.append(table_name)  # 将还在用的表加入list_clean列表，下方只是清空这些表
        for i4 in list_delete:
            cur1.execute('drop table %s' % i4)
            print u'已删除表%s' % i4
        for i5 in list_clean:
            cur1.execute('delete from %s' % i5)
            print u'已清空表%s' % i5


def clean_user(nick):
    cur1 = msql()
    id = get_sqldata('accounts', 'nick', nick, 'user_id')   # 通过传进来的nick，获得这个用户的id
    if id == None:
        print u'没有此用户'
        return 0
    else:
        list_userid = ('account_device_infos', 'accounts', 'addresses', 'duel_history_count', 'episode_user_footprint',
        'feedbacks', 'guess_choices', 'lottery_orders', 'market_point_history', 'notification_unread_count', 'point',
        'point_breakdown', 'point_history', 'product_orders', 'program_point_history', 'thirdparty_infos', 'today_point',
        'ugc_point_history', 'users_point_history', 'vote_choices')
        for i in list_userid:
            cur1.execute("delete from %s where user_id = '%s'" % (i, id))

        for i in ('article_like_action', 'favorites', 'info_like_actions', 'ugc_like_action', 'ugc_report'):
            cur1.execute("delete from %s where username = '%s'" % (i, id))

        for i in ('article_replies', 'ugc_post', 'ugc_reply', 'info_replies'):
            cur1.execute("delete from %s where author = '%s'" % (i, id))

        for i in ('followed', 'following', 'friends'):
            cur1.execute("delete from %s where me='%s' or target_user='%s'" % (i, id, id))

        cur1.execute("delete from relation_meta where me='%s'" % id)
        cur1.execute("delete from duel_instance where creator_id='%s' or competitor_id='%s'" % (id, id))
        cur1.execute("delete from notification where sender='%s' or receiver='%s'" % (id, id))

        d1 = cur1.query("SELECT table_name FROM information_schema.tables WHERE table_name LIKE 'event\_%%'")
        if len(d1) == 0:  # 判断是否有event开头的表
            print (u'没有event开头的表')
        else:
            for i1 in d1:
                cur1.execute("delete from `%s` where user_id= '%s'" % (i1["table_name"], id))
                print u'已清除'+nick+u'在'+i1["table_name"]+u""+u"中的数据"

        d2 = cur1.query("SELECT table_name FROM information_schema.tables WHERE table_name LIKE 'weekly\_%%'")
        if len(d2) == 0:  # 判断是否有weekly开头的表
            print (u'没有weekly开头的表')
        else:
            for i2 in d2:
                cur1.execute("delete from `%s` where user_id= '%s'" % (i2["table_name"], nick))
                print u'已清除'+nick+u'在'+i2["table_name"]+u""+u"中的数据"

        print u'删除完毕'


def clean_ugcpost():
    cur = msql()
    name = ('ugc_like_action', 'ugc_point_history', 'ugc_post', 'ugc_reply', 'ugc_report', 'ugc_report_handle')
    for i in name:
        cur.execute('delete from %s' % i)

