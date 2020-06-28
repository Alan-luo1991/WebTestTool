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
from flask import request

from flask import render_template


def con_mysql(sql):
    """
    连接mysql数据库
    :param sql: 需要执行的查询语句
    :return: 返回一行数据
    """
    db = pymysql.connect('10.0.0.32', 'root', '123456', 'game', 3306)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
    return cursor.fetchone()


def con_mongo(DBset):
    """
    连接mongoDB
    :param DBset: 表名称
    :return: 表对象
    """
    myclient = pymongo.MongoClient(host='10.0.0.252', port=27017)
    mydb = myclient['wanyu']
    mycol = mydb[DBset]
    return mycol


def gamesiteinfo(gameType):
    """
    查询游戏场次中机器人开关状态
    :param gameType: 游戏类型
    :return: 各场次机器人开关状态
    """
    Primary = con_mongo('gamekind').find_one({'gameType': gameType, 'name': '初级场'}, {'_id': 0, 'enableRobot': 1})['enableRobot']
    Intermediate = con_mongo('gamekind').find_one({'gameType': gameType, 'name': '中级场'}, {'_id': 0, 'enableRobot': 1})['enableRobot']
    Senior = con_mongo('gamekind').find_one({'gameType': gameType, 'name': '高级场'}, {'_id': 0, 'enableRobot': 1})['enableRobot']
    Master = con_mongo('gamekind').find_one({'gameType': gameType, 'name': '大师场'}, {'_id': 0, 'enableRobot': 1})['enableRobot']
    fieldresult = ['初级场：'+str(Primary), '中级场：'+str(Intermediate), '高级场：'+str(Senior), '大师场：'+str(Master)]
    return fieldresult


def updatagold_mysql(gameID, jb_num):
    """
    更新mysql数据库中的玩家金币数
    :param gameID: 玩家ID
    :param jb_num: 目标金币数
    :return:
    """
    db = pymysql.connect('10.0.0.32', 'root', '123456', 'game', 3306)
    cursor = db.cursor()
    sql = 'UPDATE user_info SET balance={} WHERE user_id={}'.format(jb_num, gameID)
    cursor.execute(sql)
    db.commit()
    db.close()

