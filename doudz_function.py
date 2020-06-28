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
import requests
import json
import public_function

# 手牌字典
dict_ddz = dict(方块A='0x01', 方块2='0x02', 方块3='0x03', 方块4='0x04', 方块5='0x05', 方块6='0x06', 方块7='0x07', 方块8='0x08',
                方块9='0x09', 方块10='0x0A', 方块J='0x0B', 方块Q='0x0C', 方块K='0x0D', 梅花A='0x11', 梅花2='0x12', 梅花3='0x13',
                梅花4='0x14', 梅花5='0x15', 梅花6='0x16', 梅花7='0x17', 梅花8='0x18', 梅花9='0x19', 梅花10='0x1A', 梅花J='0x1B',
                梅花Q='0x1C', 梅花K='0x1D', 红桃A='0x21', 红桃2='0x22', 红桃3='0x23', 红桃4='0x24', 红桃5='0x25', 红桃6='0x26',
                红桃7='0x27', 红桃8='0x28', 红桃9='0x29', 红桃10='0x2A', 红桃J='0x2B', 红桃Q='0x2C', 红桃K='0x2D', 黑桃A='0x31',
                黑桃2='0x32', 黑桃3='0x33', 黑桃4='0x34', 黑桃5='0x35', 黑桃6='0x36', 黑桃7='0x37', 黑桃8='0x38', 黑桃9='0x39',
                黑桃10='0x3A', 黑桃J='0x3B', 黑桃Q='0x3C', 黑桃K='0x3D', 小王='0x4E', 大王='0x4F')
# 斗地主游戏类型
game_dict = {'100': 'HLdoudz_extends.html', '118': 'FKdoudz_extends.html'}


def deploycard(gametype):
    """
    发送斗地主手牌配置到目标服务器
    :param gametype: 游戏类型
    :return: 返回当前渲染界面
    """
    card_str = request.form['CardName_doudz']
    card_list = card_str[:-1].split(',')
    card_ID = []
    for i in card_list:
        if i != '':
            card_ID.append(dict_ddz[i])
    gameID = str(request.form['User_Id_Data'])
    url = str(request.form['Server_Url_Data'])
    if len(card_ID) == 0:
        return render_template(game_dict[gametype], Tips='配牌不能为空！', User_id=gameID, Server_url=url)
    elif len(set(card_list)) != len(card_list):
        return render_template(game_dict[gametype], Tips='每张牌只支持配置1次，请检查配置！', User_id=gameID, Server_url=url)
    elif len(card_ID) != 17:
        return render_template(game_dict[gametype], Tips='请配置17张牌！', User_id=gameID, Server_url=url)
    # elif gameID.isnumeric() is False:
    #     return render_template('HLdoudz_extends.html', Tips='请输入正确的游戏ID！', User_id=gameID, Server_url=url)
    else:
        try:
            card_data = {'gameId': gametype, 'usersCards': [{'userId': public_function.selectid_mongo(), 'cards': card_ID}]}
            res = requests.post(url, json=card_data)
            return render_template(game_dict[gametype], Tips=res.text, User_id=gameID, Server_url=url)
        except:
            return render_template(game_dict[gametype], Tips='请检查游戏ID或者是否连接到内网！', User_id=gameID, Server_url=url)