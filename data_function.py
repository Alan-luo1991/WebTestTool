#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2020/04/21 上午 11:26
# @Author   : Alan_luo
# @Site     :
# @File     : WebTestTool.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c)  2019
# @Licence  :     <your licence>
# @Version  :   V1.0 2020/04/21 10:49
from flask import Flask
import pymongo
import pymysql

from flask import render_template


def con_mysql(sql):
    db = pymysql.connect('10.0.0.32', 'root', '123456', 'game', 3306)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
    return cursor.fetchone()


def con_mongo():
    myclient = pymongo.MongoClient(host='10.0.0.251', port=27017)
    mydb = myclient['wanke']
    mycol = mydb['gamekind']
    return mycol


def refieldinfo():
    Primary = con_mongo().find_one({'gameType': 117, 'name': '初级场'}, {'_id': 0, 'enableRobot': 1})['enableRobot']
    Intermediate = con_mongo().find_one({'gameType': 117, 'name': '中级场'}, {'_id': 0, 'enableRobot': 1})['enableRobot']
    Senior = con_mongo().find_one({'gameType': 117, 'name': '高级场'}, {'_id': 0, 'enableRobot': 1})['enableRobot']
    Master = con_mongo().find_one({'gameType': 117, 'name': '大师场'}, {'_id': 0, 'enableRobot': 1})['enableRobot']
    fieldresult = ['初级场：'+str(Primary), '中级场：'+str(Intermediate), '高级场：'+str(Senior), '大师场'+str(Master)]
    return fieldresult