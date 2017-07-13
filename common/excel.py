#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xlrd import open_workbook
import os
import collections
import json


def get_case(filename, sheetname, modu):
    common_path = os.path.dirname(os.path.abspath(__file__))
    path_case = common_path + '\\excel\\' + filename
    file = open_workbook(path_case)  # 打开excel文件
    table = file.sheet_by_name(sheetname)   # 读取excel对应sheet页的内容
    nrows = table.nrows  # 有内容的行数

    data = collections.defaultdict(list)  # 调用collections的defaultdict类，当判断到dict的key不存在时，创建这个key并给个默认值[]

    module = None
    for i in range(0, nrows):
        colnames = table.row_values(i)
        if colnames[0] and colnames[0] != module:
            colnumber= 0
            for i in colnames:  # 计算当前类包含列数
                if i:
                    colnumber = colnumber+1
            module = colnames[0]
        datatype, datarow = module, colnames[2:colnumber]
        if not datatype:  # 将case组合成{}显示出来
            continue
        data[datatype].append(datarow)
    #print json.dumps(data, indent=2)
    #print data[modu][1:]
    return data[modu][1:]

# get_excel('case_app.xls', 'ugc', 'CreatePost')

# def get_excel(filename, sheetname):
#     common_path = os.path.dirname(os.path.abspath(__file__))
#     path_case = common_path + '\\excel\\' + filename
#     file = open_workbook(path_case)  # 打开excel文件
#     table = file.sheet_by_name(sheetname)   # 读取excel对应sheet页的内容
#     nrows = table.nrows  # 有内容的行数
#
#     data = []
#     for i in range(1, nrows):
#         colnames = table.row_values(i)
#         case = colnames[0]
#         row = colnames[1:]
#         if not case:
#             continue
#         data.append(row)
#     return data


#get_excel('app.xls','ugc_create')

# class excel(object):
#     def __init__(self,filename,sheetname):
#         self.filename = filename
#         self.sheetname = sheetname
#         self.common_path = os.path.dirname(os.path.abspath(__file__))  # 去掉文件名((获取当前文件路径，包含文件名))
#         self.path_case = self.common_path + '\\excel\\' + self.filename  # 拼接出case文件夹下的某excel地址
#         self.file = open_workbook(self.path_case)  # 打开excel文件
#
#     def get_excel(self):  # 获取对应excel对应页的所有内容，按[{},{},{}]格式输出
#         table = self.file.sheet_by_name(self.sheetname)   # 读取excel对应sheet页的内容
#         nrows = table.nrows  # 行数
#         colnames = table.row_values(0)  # 第一行数据(即标题行)
#         list = []
#         for rownum in range(1, nrows):  # 从第二行开始，依次获取每行内容
#           row = table.row_values(rownum)
#           if row:
#               app = {}
#               for i in range(len(colnames)):
#                  app[colnames[i]] = row[i]
#               list.append(app)
#         return list


#a = excel('login.xls','console')
#b = a.get_excel()

