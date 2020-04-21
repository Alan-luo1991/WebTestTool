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
import pymongo
import data_function

dict_maj = dict(一万='11', 二万='12', 三万='13', 四万='14', 五万='15', 六万='16', 七万='17', 八万='18', 九万='19',
                一筒='21', 二筒='22', 三筒='23', 四筒='24', 五筒='25', 六筒='26', 七筒='27', 八筒='28', 九筒='29',
                一条='31', 二条='32', 三条='33', 四条='34', 五条='35', 六条='36', 七条='37', 八条='38', 九条='39',)
player = ''
# 取出所有的key
name_list = dict_maj.keys()


def deploycard():
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


def changecard():
    try:
        change_num = int(request.form['Change_Three_Card_Data'])
        print(change_num)
        db = pymysql.connect('10.0.0.32', 'root', '123456', 'game', 3306)
        cursor = db.cursor()
        sql = 'UPDATE xuezhandaodi SET exchange={} WHERE id between 1 and 5'.format(change_num)
        cursor.execute(sql)
        db.commit()
        db.close()
        return render_template('maj_extends.html', Tips='写入成功')
    except:
        return render_template('maj_extends.html', Tips='无法连接到数据库，请联系管理员！')


def updatagold():
    gameID = str(request.form['User_Id_Data'])
    try:
        print(gameID)
        jb_num = request.form['Gold_Number_Data']
        print(jb_num)
        db = pymysql.connect('10.0.0.32', 'root', '123456', 'game', 3306)
        cursor = db.cursor()
        sql = 'UPDATE user_info SET balance={} WHERE user_id={}'.format(jb_num, gameID)
        cursor.execute(sql)
        db.commit()
        db.close()
        return render_template('maj_extends.html', Tips='修改金币成功', User_id=gameID)
    except:
        return render_template('maj_extends.html', Tips='请检查游戏ID或者是否连接到内网', User_id=gameID)


def nextcard():
    cardpool_url = 'http://10.0.0.32:8802/user/mjAppointTakeCard'
    gameID = request.form['User_Id_Data']
    card_key = request.form['Next_Card_Data'][:-1]
    print(card_key)
    if (card_key in name_list) is False:
        return render_template('maj_extends.html', Tips='请检查配置麻将牌是否正确', User_id=gameID)
    elif len(gameID) == 0:
        return render_template('maj_extends.html', Tips='请输入正确的游戏ID', User_id=gameID)
    else:
        card = dict_maj[card_key]
        data = {'UserId': int(gameID), 'Mj': int(card[:-1])}
        req = requests.post(cardpool_url, json=data)
        if len(req.text) == len('eyJjb2RlIjoyMDAsIm1lc3NhZ2UiOiIiLCJkYXRhIjpudWxsfQ==') + 2:
            return render_template('maj_extends.html', Tips='配牌成功', User_id=gameID)
        else:
            return render_template('maj_extends.html', Tips='配牌成功！', User_id=gameID)


def ipswitch():
    switch_maj = request.form['r']
    game_site = request.form['game_site']
    myclient = pymongo.MongoClient(host='10.0.0.251', port=27017)
    mydb = myclient['wanke']
    mycol = mydb['gamekind']
    myquery = {'gameType': 117, 'name': game_site}
    if switch_maj == 'open':
        newvalue = {'$set': {'enableRobot': bool(2 > 1)}}
        mycol.update_many(myquery, newvalue)
        requests.get('http://10.0.0.204:30016/user/updategame')
        return render_template('maj_extends.html', Tips=game_site + '-->机器人已打开，现在能够匹配到机器人了',
                               fieldresult=data_function.refieldinfo())
    if switch_maj == 'close':
        newvalue = {'$set': {'enableRobot': bool(1 > 2)}}
        mycol.update_many(myquery, newvalue)
        requests.get('http://10.0.0.204:30016/user/updategame')
        return render_template('maj_extends.html', Tips=game_site + '-->机器人已关闭，现在无法匹配到机器人了',
                               fieldresult=data_function.refieldinfo())
