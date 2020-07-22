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

game_dict = {117: 'XZmaj_extends.html', 119: 'XLmaj_extends.html'}


def Ipstate(gametype):
    """
    IP状态查询
    :param gameType: 游戏类型
    :return:
    """
    result = data_function.con_mongo('gamekind').find_one({'gameType': gametype, 'enabled': bool(2 > 1)}, {'_id': 0, 'matchIp': 1})
    if bool(result) is False:
        IPresult = '数据库为空'
        return IPresult
    else:
        if result['matchIp'] is False:
            IPresult = '已关闭'
            return IPresult
        if result['matchIp'] is True:
            IPresult = '已打开'
            return IPresult


# def Ipswitch(gameType):


def Robotswitch(gametype):
    """
    机器人开关
    :param gametype: 游戏类型
    :return:
    """
    switch_maj = request.form['robot']
    game_site = str(request.form['game_site'])
    myquery = {'gameType': gametype, 'name': game_site}
    if switch_maj == 'open':
        newvalue = {'$set': {'enableRobot': bool(2 > 1)}}
        data_function.con_mongo('gamekind').update_many(myquery, newvalue)
        return render_template(game_dict[gametype], Tips=game_site + '-->机器人已打开，现在能够匹配到机器人了',
                               fieldresult=data_function.gamesiteinfo(gametype))
    if switch_maj == 'close':
        newvalue = {'$set': {'enableRobot': bool(1 > 2)}}
        data_function.con_mongo('gamekind').update_many(myquery, newvalue)
        return render_template(game_dict[gametype], Tips=game_site + '-->机器人已关闭，现在无法匹配到机器人了',
                               fieldresult=data_function.gamesiteinfo(gametype))


def updatagold_mongo():
    """
    更新mongoDB中用户金币
    :return:
    """
    gameID = str(request.form['User_Id_Data'])
    player_id = selectid_mongo()
    jb_num = int(request.form['Gold_Number_Data'])
    myquery = {'_id': player_id}
    newvalue ={'$set': {'money': jb_num}}
    data_function.con_mongo('playermoney').update_many(myquery, newvalue)
    return gameID


def selectid_mongo():
    """
    通过user_id查询player_id
    :param user_id: 玩家id
    :return: 返回玩家唯一标识
    """
    user_id = str(request.form['User_Id_Data'])
    try:
        player_id = data_function.con_mongo('playerdata').find_one({'userID': user_id}, {'_id': 1})
        print(player_id)
        if player_id is None:
            player_id = data_function.con_mongo252('playerdata').find_one({'userID': user_id}, {'_id': 1})
            if player_id is None:
                return "找不到对应的ID"
            else:
                return player_id['_id']
        else:
            return player_id['_id']
    except:
        return "找不到对应的ID"


# def conn_sh(url):
#     """
#     连接对应服务器地址
#     :param url:
#     :return:
#     """
