#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from common.Create import program
import myyaml
from common import session

def tab_program(tab_id,program_id):
    url = myyaml.config['domain_console'] + 'draft/pages/home/tabs/' + '%s'% tab_id + '/groups/programs/items'
    data = {
        'type': 'program',
        'ref_id': program_id
    }

    s = session.console_session()
    r = s.post(url, json = data)
    assert r.status_code

#tab_program('7f57f7a586804fb9b21cb770fde802c0','5941fb098cb51d2d70f33b21')

# def article(name,):
#     url = myyaml.config['domain_console']+'draft/articles'
#     data = {
#         'title':name,
#
#     }

def my(name):
    programid = program.create_program(name)
    program.create_episode('非直播', myid=programid, n=1, name='第一期')
    return programid



# for i in range(0,30):
#     id = my(str(i))
#     tab_program('8d3126852873402eb0a68f9265a8728a',id)



def getpostlist():
    url = myyaml.config['domain_app'] + myyaml.api['ugc_post'] + '?' + 'sort=latest'+'&'+'page_size=5'
    print url



    s = session.app_session()
    r = s.get(url)
    print r.status_code
    a = r.json()
    print len(a)
    print json.dumps(a, indent=2)

#  getpostlist()