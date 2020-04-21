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
import pymysql
import paramiko
import os.path
import time
import xlrd
import os
import svn.remote
import pymongo

dict_maj = dict(一万='11', 二万='12', 三万='13', 四万='14', 五万='15', 六万='16', 七万='17', 八万='18', 九万='19',
                一筒='21', 二筒='22', 三筒='23', 四筒='24', 五筒='25', 六筒='26', 七筒='27', 八筒='28', 九筒='29',
                一条='31', 二条='32', 三条='33', 四条='34', 五条='35', 六条='36', 七条='37', 八条='38', 九条='39',)
player = ''


def sending():
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
        return render_template('maj_extends.html', Tips='配牌不能为空！', User_id=user_id)
    elif card_max_number > 4:
        return render_template('maj_extends.html', Tips='相同牌不能超过4张！', User_id=user_id)
    elif user_id.isdigit() is False:
        return render_template('maj_extends.html', Tips='请输入正确的游戏ID！', User_id=user_id)
    else:
        try:
            card_data = {'gameId': "600102", 'usersCards': [{'userId': user_id, 'cards': card_ID}]}
            # res = requests.get(get_url)
            res = requests.post(server_url, json=card_data)
            print(server_url, card_data)
            return render_template('maj_extends.html', Tips=res.text, User_id=user_id, Player=player)
        except:
            pass