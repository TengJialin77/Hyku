#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime

def get_date(day):
    '''
    用于获得本周任何一天的日期
    :param day: 想获得星期几的日期（周一就传1）
    :return:
    '''
    today_date = datetime.date.today()  # 获得今天的日期
    today_weekday = today_date.isoweekday()  # 获得今天是星期几
    days = today_weekday-day  # 计算出今天距离想获得的那天相差的天数
    want_date = today_date - datetime.timedelta(days=days)  # 计算出想获得那天的日期
    return want_date.strftime('%Y%m%d')
