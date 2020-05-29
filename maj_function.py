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
from flask import render_template
from flask import request
import requests
import json
import pymysql
import pymongo
import data_function
import public_function

dict_maj = dict(一万='11', 二万='12', 三万='13', 四万='14', 五万='15', 六万='16', 七万='17', 八万='18', 九万='19',
                一筒='21', 二筒='22', 三筒='23', 四筒='24', 五筒='25', 六筒='26', 七筒='27', 八筒='28', 九筒='29',
                一条='31', 二条='32', 三条='33', 四条='34', 五条='35', 六条='36', 七条='37', 八条='38', 九条='39',)
player = ''
# 取出所有的key
name_list = dict_maj.keys()


def deploycard():
    """
    发送配置到服务器
    :return:
    """
    global player
    if len(player) > 1000:
        player = ''
    card_str = request.form['Card_Name']
    card_list = card_str[:-1].split(',')
    card_ID = []
    for i in card_list:
        if i != '':
            card_ID.append(dict_maj[i])
    # card_list = ''.join(dict_maj[i] for i in request.form['Card_Name'][:-1].split(',') if i != '')
    user_id = str(request.form['User_Id_Data'])
    server_url = str(request.form['Server_Url_Data'])
    # get_url = server_url + '?user_id=' + user_id + '&maj=' + card_list[:-1]
    a = '游戏ID->' + user_id + '：' + request.form['Card_Name'] + '\n'
    player += a
    statis_card_number = {}
    card_max_number = 0
    for i in request.form['Card_Name'][:-1].split(','):
        statis_card_number[i] = request.form['Card_Name'][:-1].split(',').count(i)
    for key, value in statis_card_number.items():
        if value > card_max_number:
            card_max_number = value
    if card_list == '':
        return render_template('XZmaj_extends.html', Tips='配牌不能为空！', User_id=user_id)
    elif card_max_number > 4:
        return render_template('XZmaj_extends.html', Tips='相同牌不能超过4张！', User_id=user_id)
    # elif user_id.isdigit() is False:
    #     return render_template('XZmaj_extends.html', Tips='请输入正确的游戏ID！', User_id=user_id)
    else:
        try:
            card_data = {'gameId': "600102", 'usersCards': [{'userId': public_function.selectid_mongo(), 'cards': card_ID}]}
            res = requests.post(server_url, json=card_data)
            print(server_url, card_data)
            return render_template('XZmaj_extends.html', Tips=res.text, User_id=user_id, Player=player)
        except:
            pass


def changecard():
    """
    发送换三张配置到服务器
    :return:
    """
    try:
        change_num = int(request.form['Change_Three_Card_Data'])
        server_url = 'http://10.0.0.32:8080/game/setXzddExchange'
        data = {"exchange": int(change_num)}
        res = requests.post(server_url, json=data)
        return render_template('XZmaj_extends.html', Tips=res.text)
    except:
        return render_template('XZmaj_extends.html', Tips='无法连接到数据库，请联系管理员！')


def nextcard():
    """
    发送下一张拿牌配置到服务器
    :return:
    """
    cardpool_url = 'http://10.0.0.32:8080/game/setXZDDNextCard'
    gameID = request.form['User_Id_Data']
    card_key = request.form['Next_Card_Data'][:-1]
    print(card_key)
    if (card_key in name_list) is False:
        return render_template('XZmaj_extends.html', Tips='请检查配置麻将牌是否正确', User_id=gameID)
    elif len(gameID) == 0:
        return render_template('XZmaj_extends.html', Tips='请输入正确的游戏ID', User_id=gameID)
    else:
        card = dict_maj[card_key]
        data = {'userId': gameID, 'card': card}
        req = requests.post(cardpool_url, json=data)
        reqdata = json.loads(req.text)
        return render_template('XZmaj_extends.html', Tips=reqdata["data"], User_id=gameID)
