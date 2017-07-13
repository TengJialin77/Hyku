#!/usr/bin/env python
# -*- coding: utf-8 -*-


import myyaml
import random
from common import session, image


def create_merchant(name=None):
    '''
    :param name: 店铺名字（不传用随机值）
    :return:
    '''

    url = myyaml.config['domain_merchant'] + myyaml.api['merchant']
    if name:
        merchant_name = name
    else:
        merchant_name = u'藤藤的第 %s 个商品屋' % random.randint(0, 100)
    merchant_address = u'成都市高新区茂业中心B座2703'
    phone = '86-13458650253'
    email = 'jialin.teng@hyku.com'
    policy = u'这里是滕滕的商品屋，规则如下：不帅的不准买！'
    payment_channel = {
        'id': 'doku',
        'mall_id': '4014',
        'shared_key': 'oT2i7Jo2R4iF',
        'public_key': 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6KV608l/uW6mDwKW+fCMAdA7ebSN8EVNGO6FplGXxXbnEnKSIuQyWCcNNtunzYc3IWQ6y5MI2oNxWjJIPuCeyjkruWdvOLbWVsJMKo8wpN+AbjNcX7s/G5CiNZblt2N9342mGarDQIMlhu3htqLKERTJJ34fuOND9sHY04I7agE0zFhYjfAsyyeCtF3gs+w5l4NFkIeCwKzpP1Kl/VU1Ohe5iafqARmxn1FwlEPWc/eA/y3kOGICnDZiIXjV5mbwn3kISzXcwXjjZMAQbLE1iBVJxV677IS6DuYniIWfbi/GJ1Yy6DOGOtH9f3M5pagJaSFodPCYSnqwexnBFs9D3wIDAQAB'
    }

    create_data = {
        'name': merchant_name,
        'address': merchant_address,
        'phone': phone,
        'email': email,
        'policy': policy,
        'payment': [payment_channel]
        }

    s = session.merchant_session()
    r = s.post(url, json=create_data)
    assert r.status_code == 200
    print u'创建店铺 %s 成功' % merchant_name

    merchant_id = r.json()['id']
    return merchant_id
def get_merchant_id():
    url = myyaml.config['domain_merchant'] + myyaml.api['merchant']
    s = session.merchant_session()
    r = s.get(url).json()

    if len(r) == 0:
        merchant_id = create_merchant()
    else:
        merchant_id = r[0]['id']

    return merchant_id


def create_SPU(id=None, name=None):
    '''
    :param id: 店铺id（不传获取第一个店铺id，一个店铺都没有，新创建一个店铺）
    :param name: SPU名字（不传随机值）
    :return:
    '''

    if id:
        merchant_id = id
    else:
        merchant_id = get_merchant_id()
    url = myyaml.config['domain_merchant'] + myyaml.api['spu'].format(merchant_id=merchant_id)

    if name:
        spu_name = name
    else:
        spu_name = u'我的SPU %s' % random.randint(0, 100)

    abstract = u'这里是Textual description，竖屏横屏都会显示！！'
    description = u'这里是Detailed descriptions，只有竖屏才会显示'
    banner = [image.upload_image_merchant(), image.upload_image_merchant(), image.upload_image_merchant()]

    data = {
        'name': spu_name,
        'abstract': abstract,
        'description': description,
        'banner': banner,
        'thumbnail': {
            'normal': image.upload_image_merchant(),
            'live': image.upload_image_merchant()
        }
    }

    s = session.merchant_session()
    r = s.post(url, json=data)
    assert r.status_code == 200
    print u'在merchant(%s)下，创建SPU (%s) 成功' % (merchant_id, spu_name)

    spu_id = r.json()['id']
    return spu_id
def get_spu_id(id=None):
    '''
    :param id: 店铺id（不传获取第一个店铺id，一个店铺都没有，新创建一个店铺）
    :return:
    '''
    if id:
        merchant_id = id
    else:
        merchant_id = get_merchant_id()

    url = myyaml.config['domain_merchant'] + myyaml.api['spu'].format(merchant_id=merchant_id)

    s = session.merchant_session()
    r = s.get(url).json()

    if len(r) == 0:
        spu_id = create_SPU(merchant_id)
    else:
        spu_id = r[0]['id']

    return spu_id


def create_attributes(id=None,name=None):
    '''
    :param id: 店铺id（不传获取第一个店铺id，一个店铺都没有，新创建一个店铺）
    :param name: 属性名字（不传随机值）
    :return:
    '''
    if id:
        merchant_id = id
    else:
        merchant_id = get_merchant_id()

    if name:
        attributes_name = name
    else:
        attributes_name = u'藤藤的属性%s' % random.randint(0,1000)

    url = myyaml.config['domain_merchant'] + myyaml.api['attributes'].format(merchant_id=merchant_id)
    data = {
        'name': attributes_name
    }

    s = session.merchant_session()
    r = s.post(url, json=data)
    assert r.status_code == 200

    attributes_id = r.json()['id']
    return attributes_id
def get_attributes_id(id=None):
    '''
    :param id:  店铺id（不传获取第一个店铺id，一个店铺都没有，新创建一个店铺）
    :return:
    '''
    if id:
        merchant_id = id
    else:
        merchant_id = get_merchant_id()

    url = myyaml.config['domain_merchant'] + myyaml.api['attributes'].format(merchant_id=merchant_id)

    s = session.merchant_session()
    r = s.get(url).json()

    if len(r) == 0:
        attributes_id = create_attributes(merchant_id)
    else:
        attributes_id = r[0]['id']

    return attributes_id


def create_SKU(price=None,MerchantId=None, SpuId=None):
    '''
    :param price: 单价 **元
    :param MerchantId: 店铺id（不传获取第一个店铺id，一个店铺都没有，新创建一个店铺）
    :param SpuId: SPU id（不传获取第一spu的id，一个spu都没有，新创建一个spu）
    :return:
    '''

    if MerchantId:
        merchant_id = MerchantId
    else:
        merchant_id = get_merchant_id()

    if SpuId:
        spu_id = SpuId
    else:
        spu_id = get_spu_id(merchant_id)

    if price:
        sku_price = int(price)*100
    else:
        sku_price = 200*100

    url = myyaml.config['domain_merchant'] + myyaml.api['sku'].format(merchant_id=merchant_id, spu_id=spu_id)

    title = 'MySKU title %s ' % random.randint(0, 100)

    price = {
        'amount': sku_price,
        'currency': 'IDR'
    }
    # attributes = [{
    #     'id': get_attributes_id(merchant_id)
    # }]

    data = {
        'title': title,
        'price': price
        #'attributes': attributes
    }

    s = session.merchant_session()
    r = s.post(url, json=data)
    assert r.status_code == 200

    sku_id = r.json()['id']
    print u'在merchant(%s),SPU(%s)下，创建SKU (%s) 成功' % (merchant_id, spu_id, sku_id)
    return sku_id


#create_SKU(price = 100, SpuId='db81782c3eaf42eeb07b6259f441fd46')
