#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import random  # 取随机值需要
import time  # 获取当前的utc时间需要
import myyaml
from common.Create import review, channel, merchant, id, articles
from common import image, session


def create_program(name=None, imagename=None):
    '''
    创建节目
    :param name: 节目名字，不传按固定格式组合显示
    :param imagename: 图片名字，不传随机选一张
    :return:
    '''

    url = myyaml.config['domain_console'] + myyaml.api['program']
    program_id = id.create_id('program')
    if name:
        program_name = name
    else:
        program_name = 'MyProgram %s' % random.randint(0, 1000)
    channel_id = channel.get_channel_id()
    program_introduction = u'这里是 %s 的详情介绍!' % program_name
    freq_type = 'weekly'
    weekday = 'friday'
    program_showTime = long(time.time() * 1000)  # 设置program播出时间为：创建这个program的当前时间
    program_banner = image.upload_image_console()
    program_tag = [program_name]

    data = {'id': program_id,
            'name': program_name,
            'channel_id': channel_id,
            'introduction': program_introduction,
            'freq_type': freq_type,
            'weekday': weekday,
            'show_time': program_showTime,
            'banner': program_banner,
            'tags': program_tag,
            }

    s = session.console_session()
    r = s.post(url, json=data)
    assert r.status_code == 200

    review.review('program', program_id)  # 提交审核并审核通过

    print u'创建节目 %s 成功，id为 %s' % (program_name, program_id)
    return program_id


def create_episode(type, myid=None, n=None, name=None, imagename=None):
    '''
    创建episode
    :param type: ‘非直播’,‘直播’
    :param myid: program id，不传新建一个program并获取id
    :param n: 开播时间，距离当前时间的分钟数，不传默认1分钟
    :param name: episode名字，不传按固定格式组合显示
    :return:
    '''

    url = myyaml.config['domain_console'] + myyaml.api['episode']
    episode_id = id.create_id('episode')
    if myid:
        program_id = myid
    else:
        program_id = create_program()

    if name:
        episode_name = name
    else:
        episode_name = 'MyEpisode %s' % random.randint(0, 100)

    if n:
        episode_showTime = long(time.time() * 1000 + 60000 * long(n))  # n分钟后播出
    else:
        episode_showTime = long(time.time() * 1000 + 60000 * long(1))  # 没有传入播出时间，默认1分钟后

    duration = long(3600000)  # 播出时长=1小时
    episode_cover = image.upload_image_console()

    data_normal = {
            'id': episode_id,
            'name': episode_name,
            'show_time': episode_showTime,
            'duration': duration,
            'cover': episode_cover,
            'program_id': program_id,
            'type': 'normal'
    }

    data_live = {
        'id': episode_id,
        'name': episode_name,
        'show_time': episode_showTime,
        'duration': duration,
        'cover': episode_cover,
        'program_id': program_id,
        'type': 'live',
        'live': {'source': 'https://www.youtube.com/watch?v=cqvjT1D_VHs'}
    }

    if type == '非直播':
        data = data_normal
    elif type == '直播':
        data = data_live
    else:
        raise ValueError('invalid info type')

    s = session.console_session()
    r = s.post(url, json=data)
    assert r.status_code

    review.review('episode', episode_id)  # 提交审核并审核通过

    print u'创建期 %s 成功，id为 %s' % (episode_name, episode_id)
    return episode_id


def create_info(myid, product_id=None, push=None, type='图文-无横屏', name=None, landscape=100, guess_endtime=20, announce_endtime=20,
                description=u'1982年3月24日出生于台湾澎湖,出演了首部电视剧《爱情白皮书》 而踏入演艺圈。', cover_image=None, article_id=None):
    '''
    :param myid:episode id
    :param push: 推送的具体秒数,'及时'（不传或传空字符串：非直播episode，offset=null）
    :param type:  '图文-无横屏'，'图文-有横屏'，'竞猜'，'投票'
    :param name: info名字（不传按组合格式显示）
    :param landscape: info显示秒数
    :param guess_endtime：竞猜结束的秒数
    :param announce_endtime：竞猜结束到竞猜揭晓答案中间的秒数
    :param description: 竞猜描述
    :param cover_image: 图片名字
    :param article_id:文章id
    :return:
    '''

    info_id = id.create_id('info')
    episode_id = myid

    if name:
        info_name = name
    elif push == u'及时':
        info_name = type + ' ' + u'及时推送'
    elif push is None or push == '':
        info_name = type + ' ' + '(' + u'推送时间：null' + ')'
    else:
        info_name = type + ' ' + '(' + u'推送时间：' + str(push) + u'秒' + ')'

    if push == u'及时':
        push_type = 'instant'
        info_offset = None
        info_guess_endtime = long(guess_endtime * 1000)
    elif push is None or push == '':
        push_type = 'normal'
        info_offset = None
        info_guess_endtime = long(guess_endtime * 1000)
    else:
        push_type = 'normal'
        info_offset = long(int(push) * 1000)
        info_guess_endtime = long(guess_endtime * 1000)

    if type == '商品':
        if product_id:
            spu_id = product_id
        else:
            spu_id = merchant.get_spu_id()
    else:
        spu_id = None

    if type == '文章-无横屏' or type == '文章-有横屏':
        if article_id:
            articleid = article_id
        else:
            articleid = articles.get_articles_id()
    else:
        articleid = None

    share_title = 'share_title:%s' % info_name
    share_text = 'share_text:%s' % info_name
    share_image = image.upload_image_console('share.jpg')
    info_announce_endtime = long(announce_endtime * 1000)
    info_shu_content = u'这里是竖屏info detail'
    info_heng_content = u'这里是横屏info detail'

    if name == '赢0分':
        point1 = long(0)
        point2 = long(0)
    else:
        point1 = long(100)
        point2 = long(50)

    base_data = {'id': info_id,
                 'episode_id': episode_id,
                 'name': info_name,
                 'push_type': push_type,
                 'offset': info_offset,
                 'share': {'title': share_title, 'text': share_text, 'image': share_image},
                 }

    landscape_shu = {
        'landscape': {
            'duration': landscape*1000
        }
    }
    landscape_heng = {
        'landscape': {
            'duration': landscape*1000,
            'image': image.upload_image_console(),
            'content': info_heng_content
        }
    }

    standard_data = {
        'type': 'standard',
        'image': image.upload_image_console(cover_image),
        'content': info_shu_content,
    }

    guess_data = {
        'type': 'timingGuess',
        'guess_period': info_guess_endtime,
        'announce_period': info_announce_endtime,
        'question': info_name,
        'description': description,
        'answers': [u'彭于晏', u'明道', u'阮经天', u'陆毅', u'张智霖', u'胡歌', u'霍建华', u'靳东',u'冯绍峰'],
        'right_answer': 0,
        'points': point1,
        'overtime_compensation': point2
    }

    vote_data = {
        'type': 'vote',
        'deadline': long(time.time() * 1000 + 3600000),
        'question': info_name,
        'answers': [u'彭于晏', u'明道', u'阮经天', u'陆毅', u'张智霖' u'胡歌', u'霍建华', u'靳东',u'冯绍峰']
    }

    product_data = {
        'type': 'product',
        'thumbnail': image.upload_image_merchant(),
        'product_id': spu_id
    }

    article_data = {
        'type': 'article',
        'image': image.upload_image_console(),
        'article_id': articleid
    }

    if type == '图文-无横屏':
        data = dict(base_data.items() + landscape_shu.items() + standard_data.items())
    elif type == '图文-有横屏':
        data = dict(base_data.items() + landscape_heng.items() + standard_data.items())
    elif type == '竞猜':
        data = dict(base_data.items() + landscape_shu.items() + guess_data.items())
    elif type == '投票':
        data = dict(base_data.items() + landscape_shu.items() + vote_data.items())
    elif type == '商品':
        data = dict(base_data.items() + landscape_shu.items() + product_data.items())
    elif type == '文章-无横屏':
        data = dict(base_data.items() + landscape_shu.items() + article_data.items())
    elif type == '文章-有横屏':
        data = dict(base_data.items() + landscape_heng.items() + article_data.items())
    else:
        raise ValueError('invalid info type')

    url = myyaml.config['domain_console'] + myyaml.api['info']
    s = session.console_session()
    r = s.post(url, json=data)
    assert r.status_code == 200
    review.review('info', info_id)

    print u'创建info %s 成功，id为 %s' % (info_name, info_id)

#create_info('595de70d8cb51d1f925b17c4', type='文章-有横屏')
