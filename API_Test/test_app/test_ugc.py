#!/usr/bin/env python
# -*- coding: utf-8 -*-


import myyaml
import pytest
from common import image, session
from common import excel, myredis

case_uploadimage = excel.get_case('case_app.xls', 'ugc', 'UploadImage')
case_create = excel.get_case('case_app.xls', 'ugc', 'CreatePost')


# 测试创建post时上传图片到S3服务器的接口
@pytest.mark.parametrize('type, imagename,code', case_uploadimage)
def test_uploadimage(type, imagename, code):
    url = myyaml.config['domain_app'] + myyaml.api['upload_image_ugcpost']
    data = {
        'files': [
            {'name': imagename,
             'type': 'image'
             }
        ]
    }
    s = session.app_session()

    r = s.post(url, json=data, headers={'X-ClientVersion': '2.5.5'})
    assert r.status_code == 200
    resp = r.json()['files'][0]
    upload_url = resp['upload_url']
    fields = resp['fields']

    path = image.image_local_path(imagename)
    with open(path, 'rb') as fd:  # 这样用可以用完自动关闭掉这个文件
        r1 = s.post(upload_url, data=fields, files={"file": fd})
    assert r1.status_code == code


# 测试创建post接口
@pytest.mark.parametrize('type,imagename,content,tag,code', case_create)
def test_create(type, imagename, content, tag, code):
    url = myyaml.config['domain_app'] + myyaml.api['ugc_post']
    name = image.upload_image_post(imagename)

    if type == 'notag':
        data = {
            'content': content,
            'resources': [
                {
                    'url': name,
                    'type': 'image',
                    'meta': {'height': 200, 'width': 300}
                }
            ]
        }
    elif type == 'nocontent':
        data = {
            'resources': [
                {
                    'url': name,
                    'type': 'image',
                    'meta': {'height': 200, 'width': 300}
                }
            ],
            'tags': [tag]
        }
    elif type == 'nullresources':
        data = {
            'content': content,
            'resources': [],
            'tags': [tag]
        }
    elif type == 'noresources':
        data = {
            'content': content,
            'tags': [tag]
        }

    elif type == 'manyimages':
        data = {
            'content': content,
            'resources': [
                {
                    'url': image.upload_image_post('ugc_normal.jpg'),
                    'type': 'image',
                    'meta': {'height': 200, 'width': 300}
                },
                {
                    'url': image.upload_image_post('ugc_normal2.jpg'),
                    'type': 'image',
                    'meta': {'height': 200, 'width': 300}
                },
                {
                    'url': image.upload_image_post('ugc_normal3.jpg'),
                    'type': 'image',
                    'meta': {'height': 200, 'width': 300}
                }
            ],
            'tags': [tag]
        }
    elif type == 'manytags':
        data = {
            'content': content,
            'resources': [
                {
                    'url': name,
                    'type': 'image',
                    'meta': {'height': 200, 'width': 300}
                }
            ],
            'tags': ['tag1', 'tag2', 'tag3']
        }
    else:
        data = {
            'content': content,
            'resources': [
                {
                    'url': name,
                    'type': 'image',
                    'meta': {'height': 200, 'width': 300}
                }
            ],
            'tags': [tag]
        }

    s = session.app_session()
    if type == 'out':
        myredis.set_ugcpost_limitnumber(myyaml.config['ugc_posts'], 0)
    else:
        myredis.set_ugcpost_limitnumber(myyaml.config['ugc_posts'], 100)
    r = s.post(url, json=data)
    myredis.delete_ugcpost()
    assert r.status_code == code


# def test_getpostlist():
#     url = myyaml.config['domain_app'] + myyaml.api['ugc_post']
#
#     data = {
#         'sort': 'latest'
#     }
#
#     s = session.app_session()
#     r = s.get(url, json=data)
#     print r.status_code
#     print r.json()
#
# test_getpostlist()