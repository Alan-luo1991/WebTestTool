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

from flask import render_template
from flask import request
import data_function
import requests
import pymysql


def Ipstate(gameType):
    result = data_function.con_mongo().find_one({'gameType': gameType, 'enabled': bool(2 > 1)}, {'_id': 0, 'matchIp': 1})
    if result['matchIp'] is False:
        IPresult = '已关闭'
        return IPresult
    if result['matchIp'] is True:
        IPresult = '已打开'
        return IPresult


# def Ipswitch(gameType):



def Robotswitch(gameType):
    switch_maj = request.form['robot']
    game_site = request.form['game_site']
    myquery = {'gameType': gameType, 'name': game_site}
    if switch_maj == 'open':
        newvalue = {'$set': {'enableRobot': bool(2 > 1)}}
        data_function.con_mongo().update_many(myquery, newvalue)
        requests.get('http://10.0.0.204:30016/user/updategame')
        return render_template('XZmaj_extends.html', Tips=game_site + '-->机器人已打开，现在能够匹配到机器人了',
                               fieldresult=data_function.gamesiteinfo(gameType))
    if switch_maj == 'close':
        newvalue = {'$set': {'enableRobot': bool(1 > 2)}}
        data_function.con_mongo().update_many(myquery, newvalue)
        requests.get('http://10.0.0.204:30016/user/updategame')
        return render_template('XZmaj_extends.html', Tips=game_site + '-->机器人已关闭，现在无法匹配到机器人了',
                               fieldresult=data_function.gamesiteinfo(gameType))