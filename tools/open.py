#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import myyaml

from PyQt4 import QtGui  # pyqt相关函数
from ui import Ui_MainWindow  # 引用从pyqt自动生成的界面代码ui.py里面的函数

from common import database, myredis
from common.Create import program, merchant, duel, event, ugc_post


reload(sys)
sys.setdefaultencoding('utf-8')


class MyWindow(Ui_MainWindow,QtGui.QMainWindow): #创建MyWindow类，直接继承从pyqt那边自动创建的类
    def __init__(self,parent = None):
        super(MyWindow,self).__init__()
        self.setupUi(self)

        # 清空数据库
        self.Ddata.clicked.connect(self.clean_data)
        # 清空redis
        self.Dredis.clicked.connect(self.clean_redis)
        # 删除user
        self.Duser.clicked.connect(self.clean_user)
        # 创建：单个program
        self.button_CreateProgram.clicked.connect(self.create_program)
        # 创建：单个非直播episode
        self.button_CreateEpisode_nomal.clicked.connect(self.create_episode_normal)
        # 创建：单个直播episode
        self.button_CreateEpisode_live.clicked.connect(self.create_episode_live)
        # 创建：单个竞猜
        self.button_CreateGuess.clicked.connect(self.create_guess)
        # 创建：单个投票
        self.button_CreateVote.clicked.connect(self.create_vote)
        # 创建：单个图文-无横屏
        self.button_CreateStand_unlandscape.clicked.connect(self.create_stand_shu)
        # 创建：单个图文-有横屏
        self.button_CreateStand_landscape.clicked.connect(self.create_stand_heng)
        # 创建：单个商品
        self.button_CreateProduct.clicked.connect(self.create_product)
        # 创建：单个文章-无横屏
        self.button_CreateArticle_unlandscape.clicked.connect(self.create_article_shu)
        # 创建：单个文章-有横屏
        self.button_CreateArticle_landscape.clicked.connect(self.create_article_heng)
        # 创建：all-推送
        self.button_CreatePush.clicked.connect(self.create_all_push)
        # 创建：all-横屏推送
        self.button_CreatePush_heng.clicked.connect(self.create_all_push_heng)
        # 创建：all-竞猜1
        self.button_CreateAllGuess.clicked.connect(self.create_all_guess1)
        # 创建：all-竞猜2
        self.button_CreateAllGuess_2.clicked.connect(self.create_all_guess2)
        # 创建：all-detail基本项
        self.button_CreateAllBase.clicked.connect(self.create_all_base)

        # 创建单个topic
        self.create_topic_button.clicked.connect(self.create_topic)
        # 创建单个template
        self.create_template_button.clicked.connect(self.create_template)
        # 创建all duel
        self.create_all_button_duel.clicked.connect(self.create_duel_all)

        # 创建活动-duel
        self.event_PushButton_duel.clicked.connect(self.create_event_duel)
        # 创建活动-guess
        self.event_PushButton_guess.clicked.connect(self.create_event_guess)
        # 创建活动-like
        self.event_PushButton_like.clicked.connect(self.create_event_like)
        # 创建活动-invite
        self.event_PushButton_invite.clicked.connect(self.create_event_invite)
        # 创建活动-all
        self.event_PushButton_all.clicked.connect(self.create_event_all)

        # 创建merchant
        self.button_CreateMerchant.clicked.connect(self.create_merchant)
        # 创建spu
        self.button_CreateSPU.clicked.connect(self.create_spu)
        # 创建sku
        self.button_CreateSKU.clicked.connect(self.create_sku)

    def clean_user(self):
        region = str(self.region_box.currentText())  # 获取用户选择的环境
        nick = str(self.nick.text())  # 获取用户填写的需要删除的用户昵称
        myyaml.set_region(region)  # 将整个程序运行环境设置成用户选择的环境
        database.clean_user(nick)  # 删除对应用户

    def clean_data(self):
        region = str(self.region_box.currentText())  # 获取用户选择的环境
        myyaml.set_region(region)  # 将整个程序运行环境设置成用户选择的环境
        database.clean_all()  # 清空所有数据

    def clean_redis(self):
        region = str(self.region_box.currentText())  # 获取用户选择的环境
        myyaml.set_region(region)  # 将整个程序运行环境设置成用户选择的环境
        myredis.clean_redis()

    def create_program(self):
        region = str(self.region_box.currentText())  # 获取用户选择的环境
        myyaml.set_region(region)  # 将整个程序运行环境设置成用户选择的环境
        program_name = str(self.lineEdit_ProgramName.text())  # 获取用户写入的program名字
        program.create_program(program_name)   # 创建program

    def create_episode_normal(self):
        region = str(self.region_box.currentText())  # 获取用户选择的环境
        myyaml.set_region(region)  # 将整个程序运行环境设置成用户选择的环境
        program_id = str(self.lineEdit_ProgramID.text())  # 获取用户写入的program id
        episode_name = str(self.lineEdit_EpisodeName.text())  # 获取用户写入的episode名字
        episode_time = self.lineEdit_EpisodeTime.text()  # 获取用户写入的episode过期分钟数
        program.create_episode('非直播', program_id, episode_time, episode_name)  # 创建非直播episode

    def create_episode_live(self):
        region = str(self.region_box.currentText())  # 获取用户选择的环境
        myyaml.set_region(region)  # 将整个程序运行环境设置成用户选择的环境
        program_id = str(self.lineEdit_ProgramID.text())  # 获取用户写入的program id
        episode_name = str(self.lineEdit_EpisodeName.text())  # 获取用户写入的episode名字
        episode_time = self.lineEdit_EpisodeTime.text()  # 获取用户写入的episode过期分钟数
        program.create_episode('直播', program_id, episode_time, episode_name)  # 创建非直播episode

    def info_only(self, type, product_id=None, article_id=None):
        region = str(self.region_box.currentText())  # 获取用户选择的环境
        myyaml.set_region(region)  # 将整个程序运行环境设置成用户选择的环境
        episode_id = str(self.lineEdit_EpisodeID.text())  # 获取用户写入的episode id
        info_name = str(self.lineEdit_InfoName.text())  # 获取用户写入的info名字
        push = str(self.lineEdit_PushType.text())  # 获取用户写入的推送类型
        program.create_info(myid=episode_id, product_id=product_id, push=push, type=type, name=info_name, article_id=article_id)  # 创建info

    def create_guess(self):
        self.info_only('竞猜')

    def create_vote(self):
        self.info_only('投票')

    def create_stand_shu(self):
        self.info_only('图文-无横屏')

    def create_stand_heng(self):
        self.info_only('图文-有横屏')

    def create_product(self):
        product_id = str(self.lineEdit_productid.text())
        self.info_only('商品', product_id)

    def create_article_shu(self):
        article_id = str(self.lineEdit_articleid.text())
        self.info_only('文章-无横屏', article_id=article_id)

    def create_article_heng(self):
        article_id = str(self.lineEdit_articleid.text())
        self.info_only('文章-有横屏', article_id=article_id)

    def create_all_push(self):
        region = str(self.region_box.currentText())  # 获取用户选择的环境
        myyaml.set_region(region)  # 将整个程序运行环境设置成用户选择的环境
        program_id = str(self.lineEdit_ProgramID_2.text())
        type = str(self.comboBox_EpisodeType.currentText())

        episode_id = program.create_episode(type, program_id, 2)

        program.create_info(episode_id, type='图文-无横屏', name='1')
        program.create_info(episode_id, type='文章-有横屏',  name='2')
        program.create_info(episode_id, type='投票',  name='3')
        program.create_info(episode_id, type='商品',  name='4')
        program.create_info(episode_id, push=0, type='竞猜')
        program.create_info(episode_id, push=10, type='竞猜')
        program.create_info(episode_id, push=20, type='竞猜')
        program.create_info(episode_id, push=30, type='图文-无横屏')
        program.create_info(episode_id, push=40, type='图文-无横屏')
        program.create_info(episode_id, push=50, type='图文-有横屏')
        program.create_info(episode_id, push=60, type='投票')
        program.create_info(episode_id, push=70, type='投票')
        program.create_info(episode_id, push=80, type='投票')
        program.create_info(episode_id, push=90, type='文章-无横屏')
        program.create_info(episode_id, push=100, type='文章-无横屏')
        program.create_info(episode_id, push=110, type='文章-有横屏')
        program.create_info(episode_id, push=120, type='商品')
        program.create_info(episode_id, push=130, type='商品')
        program.create_info(episode_id, push=140, type='商品')
        program.create_info(episode_id, push='及时', type='图文-无横屏')
        program.create_info(episode_id, push='及时', type='图文-有横屏')

    def create_all_push_heng(self):
        region = str(self.region_box.currentText())  # 获取用户选择的环境
        myyaml.set_region(region)  # 将整个程序运行环境设置成用户选择的环境
        program_id = str(self.lineEdit_ProgramID_2.text())
        type = str(self.comboBox_EpisodeType.currentText())

        episode_id = program.create_episode('直播', program_id, 2)

        program.create_info(episode_id, push=10, type='图文-无横屏', name='图文-无横屏：推送10s，显示2s', landscape=2,)
        program.create_info(episode_id, push=20, type='图文-无横屏', name='图文-无横屏：推送20s，显示5s', landscape=5)
        program.create_info(episode_id, push=30, type='图文-有横屏', name='图文-有横屏：推送30s，显示20s', landscape=20)
        program.create_info(episode_id, push=40, type='投票', name='投票1：推送40s，显示20s', landscape=20)
        program.create_info(episode_id, push=40, type='投票', name='投票2：推送40s，显示20s', landscape=20)
        program.create_info(episode_id, push=40, type='投票', name='投票3：推送40s，显示20s', landscape=20)
        program.create_info(episode_id, push=60, type='竞猜', name='竞猜1：推送60s，显示20s', landscape=20)
        program.create_info(episode_id, push=80, type='竞猜', name='竞猜2：推送80s，显示20s', landscape=20)
        program.create_info(episode_id, push=100, type='竞猜', name='竞猜3：推送100s，显示20s', landscape=60)
        program.create_info(episode_id, push=120, type='商品', name='商品1：推送120s，显示60s', landscape=60)
        program.create_info(episode_id, push=140, type='文章-无横屏', name='图文-无横屏：推送140s，显示60s', landscape=60)
        program.create_info(episode_id, push=140, type='文章-有横屏', name='图文-无横屏：推送140s，显示60s', landscape=60)
        program.create_info(episode_id, push='及时', type='图文-无横屏')
        program.create_info(episode_id, push='及时', type='图文-有横屏')

    def create_all_guess1(self):
        region = str(self.region_box.currentText())  # 获取用户选择的环境
        myyaml.set_region(region)  # 将整个程序运行环境设置成用户选择的环境
        program_id = str(self.lineEdit_ProgramID_2.text())
        type = str(self.comboBox_EpisodeType.currentText())

        episode_id = program.create_episode(type, program_id, 1)

        program.create_info(episode_id, push=0, type='竞猜', name='不参与', guess_endtime=60, announce_endtime=30)
        program.create_info(episode_id, push=0,  type='竞猜', name='输', guess_endtime=60, announce_endtime=30)
        program.create_info(episode_id, push=0,  type='竞猜', name='赢', guess_endtime=60, announce_endtime=30)
        program.create_info(episode_id, push=0,  type='竞猜', name='赢0分', guess_endtime=60, announce_endtime=30)

    def create_all_guess2(self):
        region = str(self.region_box.currentText())  # 获取用户选择的环境
        myyaml.set_region(region)  # 将整个程序运行环境设置成用户选择的环境
        program_id = str(self.lineEdit_ProgramID_2.text())
        type = str(self.comboBox_EpisodeType.currentText())

        episode_id = program.create_episode(type, program_id, 2)

        program.create_info(episode_id, push=0,  type='竞猜', name='竞猜中-未参与', guess_endtime=36000, announce_endtime=20)
        program.create_info(episode_id, push=0,  type='竞猜', name='竞猜中-已参与', guess_endtime=36000, announce_endtime=20)
        program.create_info(episode_id, push=0,  type='竞猜', name='未参与-等待答案揭晓', guess_endtime=60, announce_endtime=36000)
        program.create_info(episode_id, push=0,  type='竞猜', name='已参与-等待答案揭晓', guess_endtime=60, announce_endtime=36000)
        program.create_info(episode_id, push=0,  type='竞猜', name='揭晓前参与-赢', guess_endtime=60, announce_endtime=20)
        program.create_info(episode_id, push=0,  type='竞猜', name='揭晓前参与-输', guess_endtime=60, announce_endtime=20)
        program.create_info(episode_id, push=0,  type='竞猜', name='未参与已揭晓', guess_endtime=60, announce_endtime=20)
        program.create_info(episode_id, push=0,  type='竞猜', name='揭晓后参与-赢', guess_endtime=60, announce_endtime=20)
        program.create_info(episode_id, push=0,  type='竞猜', name='揭晓后参与-输', guess_endtime=60, announce_endtime=20)

    def create_all_base(self):
        region = str(self.region_box.currentText())  # 获取用户选择的环境
        myyaml.set_region(region)  # 将整个程序运行环境设置成用户选择的环境
        program_id = str(self.lineEdit_ProgramID_2.text())
        type = str(self.comboBox_EpisodeType.currentText())

        episode_id = program.create_episode(type, program_id, 0.1)

        program.create_info(episode_id, type='图文-无横屏', name='null，标题少于1排')
        program.create_info(episode_id, type='图文-有横屏', name='null，标题很多字123！标题很多字123！标题很多字123！标题很多字123！标题很多字123！标题很多字123！标题很多字123！标题很多字123！')
        program.create_info(episode_id, push=0, type='竞猜', name='0s:问题描述都少于1排', description='description少于1排')
        program.create_info(episode_id, push=0, type='竞猜',name='0s:问题描述都很多字，问题描述都很多字，问题描述都很多字，问题描述都很多字，问题描述都很多字，问题描述都很多字，问题描述都很多字，问题描述都很多字，问题描述都很多字，问题描述都很多字，问题描述都很多字',description='description有很多字123！description有很多字123！description有很多字123！description有很多字123！description有很多字123！description有很多字123！description有很多字123！description有很多字123！')
        program.create_info(episode_id, push=0, type='投票', name='0s:问题很少字，没有描述')
        program.create_info(episode_id, push=0, type='投票', name='0s:问题很多字，没有描述（这里很多字！这里很多字！这里很多字！这里很多字！这里很多字！这里很多字！这里很多字！这里很多字！）')
        program.create_info(episode_id, push=10, type='图文-无横屏', name='图文10s'),
        program.create_info(episode_id, push=20, type='图文-有横屏', name='图文30s'),
        program.create_info(episode_id, push=30, type='文章-无横屏', name='文章10s'),
        program.create_info(episode_id, push=40, type='文章-有横屏', name='文章30s'),
        program.create_info(episode_id, push=50, type='商品',name='50s'),
        program.create_info(episode_id, push=60, type='竞猜', name='1分0s'),
        program.create_info(episode_id, push=3690, type='投票',name='61分30s')


    def create_topic(self):
        region = str(self.region_box.currentText())  # 获取用户选择的环境
        myyaml.set_region(region)  # 将整个程序运行环境设置成用户选择的环境
        topic_name = str(self.lineEdit_TopicName.text())
        duel.create_topic(topic_name)

    def create_template(self):
        region = str(self.region_box.currentText())  # 获取用户选择的环境
        myyaml.set_region(region)  # 将整个程序运行环境设置成用户选择的环境
        topic_id = str(self.lineEdit_TopicId.text())
        deadline = str(self.lineEdit_deadline.text())
        tempalte_name = str(self.lineEdit_TemplateName.text())
        duel.create_template(topic_id, deadline, tempalte_name)

    def create_duel_all(self):
        region = str(self.region_box.currentText())  # 获取用户选择的环境
        myyaml.set_region(region)  # 将整个程序运行环境设置成用户选择的环境
        id = str(self.lineEdit_TopicId_2.text())

        if id:
            topic_id = id
        else:
            topic_id = duel.create_topic(u'很多template，随便选择哦')

        duel.create_template(topic_id, 2)
        duel.create_template(topic_id, 4)
        duel.create_template(topic_id, 6)
        duel.create_template(topic_id, 8)
        duel.create_template(topic_id, 10)
        duel.create_template(topic_id, 12)
        duel.create_template(topic_id, 14)
        duel.create_template(topic_id, 16)
        duel.create_template(topic_id, 18)
        duel.create_template(topic_id, 20)

    def create_event_duel(self):
        event.create_event(start=-3, end=-1, name=u'duel-已结束', type='custom', custom={'duel': 'all'}, imagename='duel_end.png')
        event.create_event(start=-1, end=600, name=u'duel-活动中', type='custom', custom={'duel': 'all'}, imagename='duel_in.png')
        event.create_event(start=-600, end=300, name=u'duel-活动中1', type='custom', custom={'duel': 'all'}, imagename='duel_in1.jpg')
        event.create_event(start=600, end=601, name=u'duel-未开始', type='custom', custom={'duel': 'all'}, imagename='duel_unstart.png')

    def create_event_guess(self):
        event.create_event(start=-3, end=-1, name=u'guess-已结束', type='custom', custom={'guess': 'all'}, imagename='guess_end.png')
        event.create_event(start=-1, end=600, name=u'guess-活动中', type='custom', custom={'guess': 'all'}, imagename='guess_in.png')
        event.create_event(start=-600, end=300, name=u'guess-活动中1', type='custom', custom={'guess': 'all'}, imagename='guess_in1.png')
        event.create_event(start=600, end=601, name=u'guess-未开始', type='custom', custom={'guess': 'all'}, imagename='guess_unstart.png')

    def create_event_like(self):
        event.create_event(start=-3, end=-1, name=u'like-已结束', type='custom', custom={'ugc_like': 'all'}, imagename='like_end.png')
        event.create_event(start=-1, end=600, name=u'like-活动中', type='custom', custom={'ugc_like': 'all'}, imagename='like_in.png')
        event.create_event(start=-600, end=300, name=u'like-活动中1', type='custom', custom={'ugc_like': 'all'}, imagename='like_in1.png')
        event.create_event(start=600, end=601, name=u'like-未开始', type='custom', custom={'ugc_like': 'all'}, imagename='like_unstart.png')

    def create_event_invite(self):
        event.create_event(start=-3, end=-1, name=u'invite-已结束', type='custom', custom={'invite': 'all'}, imagename='invite_end.png')
        event.create_event(start=-1, end=600, name=u'invite-活动中', type='custom', custom={'invite': 'all'}, imagename='invite_in.png')
        event.create_event(start=-600, end=300, name=u'invite-活动中1', type='custom', custom={'invite': 'all'}, imagename='invite_in1.png')
        event.create_event(start=600, end=601, name=u'invite-未开始', type='custom', custom={'invite': 'all'}, imagename='invite_unstart.png')

    def create_event_all(self):
        event.create_event(start=-3, end=-1, name=u'all-已结束', type='custom', custom={'duel': 'all', 'ugc_like': 'all', 'guess': 'all', 'invite': 'all', 'gift': 'all'}, imagename='all_end.png')
        event.create_event(start=-1, end=600, name=u'all-活动中', type='custom', custom={'duel': 'all', 'ugc_like': 'all', 'guess': 'all', 'invite': 'all', 'gift': 'all'}, imagename='all_in.png')
        event.create_event(start=-600, end=300, name=u'all-活动中1', type='custom', custom={'duel': 'all', 'ugc_like': 'all', 'guess': 'all', 'invite': 'all', 'gift': 'all'}, imagename='all_in1.png')
        event.create_event(start=600, end=601, name=u'all-未开始', type='custom', custom={'duel': 'all', 'ugc_like': 'all', 'guess': 'all', 'invite': 'all', 'gift': 'all'}, imagename='all_unstart.png')

    def create_merchant(self):
        region = str(self.region_box.currentText())  # 获取用户选择的环境
        myyaml.set_region(region)  # 将整个程序运行环境设置成用户选择的环境
        merchant_name = str(self.lineEdit_MerchantName.text())
        merchant.create_merchant(merchant_name)

    def create_spu(self):
        region = str(self.region_box.currentText())  # 获取用户选择的环境
        myyaml.set_region(region)  # 将整个程序运行环境设置成用户选择的环境
        merchant_id = str(self.lineEdit_MerchantId.text())
        spu_name = str(self.lineEdit_SPUname.text())
        merchant.create_SPU(merchant_id, spu_name)

    def create_sku(self):
        region = str(self.region_box.currentText())  # 获取用户选择的环境
        myyaml.set_region(region)  # 将整个程序运行环境设置成用户选择的环境
        merchant_id = str(self.lineEdit_MerchantId_2.text())
        spu_id = str(self.lineEdit_SPUId.text())
        sku_price = str(self.lineEdit_Price.text())
        merchant.create_SKU(price=sku_price, MerchantId=merchant_id, SpuId=spu_id)



if __name__ =='__main__':    #展示UI界面
        app = QtGui.QApplication(sys.argv)
        main = MyWindow()
        main.show()
        sys.exit(app.exec_())
