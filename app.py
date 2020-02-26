#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/12/23 上午 11:26
# @Author   : Alan_luo
# @Site     :
# @File     : WebTestTool.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c)  2019
# @Licence  :     <your licence>
# @Version  :   V1.0 2019/12/23 10:49
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


# 实例化，可视为固定格式
app = Flask(__name__)


dict_maj = dict(一万='11,', 二万='12,', 三万='13,', 四万='14,', 五万='15,', 六万='16,', 七万='17,', 八万='18,', 九万='19,',
                一筒='21,', 二筒='22,', 三筒='23,', 四筒='24,', 五筒='25,', 六筒='26,', 七筒='27,', 八筒='28,', 九筒='29,',
                一条='31,', 二条='32,', 三条='33,', 四条='34,', 五条='35,', 六条='36,', 七条='37,', 八条='38,', 九条='39,',)


dict_ddz = dict(方块A='0x01,', 方块2='0x02,', 方块3='0x03,', 方块4='0x04,', 方块5='0x05,', 方块6='0x06,', 方块7='0x07,', 方块8='0x08,',
                方块9='0x09,', 方块10='0x0A,', 方块J='0x0B,', 方块Q='0x0C,', 方块K='0x0D,', 梅花A='0x11,', 梅花2='0x12,', 梅花3='0x13,',
                梅花4='0x14,', 梅花5='0x15,', 梅花6='0x16,', 梅花7='0x17,', 梅花8='0x18,', 梅花9='0x19,', 梅花10='0x1A,', 梅花J='0x1B,',
                梅花Q='0x1C,', 梅花K='0x1D,', 红桃A='0x21,', 红桃2='0x22,', 红桃3='0x23,', 红桃4='0x24,', 红桃5='0x25,', 红桃6='0x26,',
                红桃7='0x27,', 红桃8='0x28,', 红桃9='0x29,', 红桃10='0x2A,', 红桃J='0x2B,', 红桃Q='0x2C,', 红桃K='0x2D,', 黑桃A='0x31,',
                黑桃2='0x32,', 黑桃3='0x33,', 黑桃4='0x34,', 黑桃5='0x35,', 黑桃6='0x36,', 黑桃7='0x37,', 黑桃8='0x38,', 黑桃9='0x39,',
                黑桃10='0x3A,', 黑桃J='0x3B,', 黑桃Q='0x3C,', 黑桃K='0x3D,', 小王='0x4E,', 大王='0x4F,')
# 取出所有的key
name_list = dict_maj.keys()
player = ''


def con_mysql(sql):
    db = pymysql.connect('10.0.0.32', 'root', '123456', 'game', 3306)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
    return cursor.fetchone()


def openxl(fileurl):
    tablename = xlrd.open_workbook(fileurl)
    tablename = tablename.sheet_by_index(0)
    return tablename


# route()方法用于设定路由；类似spring路由配置
@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/homepage.html", methods=['GET', 'POST'])
def homepage():

    return render_template('homepage.html')


@app.route('/maj_extends.html', methods=['GET', 'POST'])
def maj_extends():
    global player
    if request.method == 'POST':
        if request.form['Submit_Button'] == '确认发送':
            if len(player) > 1000:
                player = ''
            card_list = ''.join(dict_maj[i] for i in request.form['Card_Name'][:-1].split(',') if i != '')
            user_id = str(request.form['User_Id_Data'])
            server_url = str(request.form['Server_Url_Data'])
            get_url = server_url + '?user_id=' + user_id + '&maj=' + card_list[:-1]
            a = '游戏ID->'+user_id+'：' + request.form['Card_Name'] + '\n'
            player += a
            print(get_url)
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
                    res = requests.get(get_url)
                    print(res.text)
                    return render_template('maj_extends.html', Tips=res.text, User_id=user_id, Player=player)
                except:
                    pass
        if request.form['Submit_Button'] == '换三张':
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
        if request.form['Submit_Button'] == '修改金币':
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
        if request.form['Submit_Button'] == '拿牌':
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
    return render_template('maj_extends.html')


@app.route('/doudz_extends.html', methods=['GET', 'POST'])
def doudz_extends():
    if request.method == 'POST':
        if request.form['Submit_Button'] == '确认发送':
            card_str = request.form['Card_Name']
            print(card_str)
            card_list = card_str[:-1].split(',')
            print(card_list)
            card_ID = ''.join(dict_ddz[i] for i in card_list if i != '')
            gameID = str(request.form['User_Id_Data'])
            url = str(request.form['Server_Url_Data'])
            if len(card_ID) == 0:
                return render_template('doudz_extends.html', Tips='配牌不能为空！', User_id=gameID, Server_url=url)
            elif len(set(card_list)) != len(card_list):
                return render_template('doudz_extends.html', Tips='每张牌只支持配置1次，请检查配置！', User_id=gameID, Server_url=url)
            # elif len(card_ID) != 95:
            #     return render_template('doudz_extends.html', Tips='请配置17张牌！', User_id=gameID, Server_url=url)
            elif gameID.isdigit() is False:
                return render_template('doudz_extends.html', Tips='请输入正确的游戏ID！', User_id=gameID, Server_url=url)
            else:
                try:
                    res = requests.get(url + '?user_id=' + gameID + '&doudizhu=' + card_ID[:-1], timeout=(3, 3))
                    # print('{}?user_id={}&doudizhu={}'.format(url, gameID, card_ID[:-1]))
                    return render_template('doudz_extends.html', Tips=res.text, User_id=gameID, Server_url=url)
                except:
                    return render_template('doudz_extends.html', Tips='请检查游戏ID或者是否连接到内网！', User_id=gameID, Server_url=url)
        if request.form['Submit_Button'] == '修改金币':
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
                return render_template('doudz_extends.html', Tips='修改金币成功', User_id=gameID)
            except:
                return render_template('doudz_extends.html', Tips='请检查游戏ID或者是否连接到内网', User_id=gameID)
    return render_template('doudz_extends.html')


@app.route('/maj_TestCoverage.html', methods=['GET', 'POST'])
def maj_TestCoverage():
    if request.method == 'GET':
        if os.path.exists('/home/test/WebTestTool/xuezhandaodi.out') is True:
            latesttime = time.ctime(os.path.getmtime('/home/test/WebTestTool/xuezhandaodi.out'))
            return render_template('maj_TestCoverage.html', LatestTime=latesttime)
    if request.method == 'POST':
        if request.form['Submit_Button'] == '下载日志':
            try:
                ser_url = paramiko.Transport('10.0.0.32', 22)
                ser_url.connect(username='testsvr', password='123456')
                sftp = paramiko.SFTPClient.from_transport(ser_url)
                sftp.get('/tmp/xuezhandaodi.out', '/home/test/WebTestTool/xuezhandaodi.out')
                latesttime = time.ctime(os.path.getmtime('/home/test/WebTestTool/xuezhandaodi.out'))
                ser_url.close()
                return render_template('maj_TestCoverage.html', Tips='下载成功', LatestTime=latesttime)
            except:
                return render_template('maj_TestCoverage.html', Tips='下载失败')
        if request.form['Submit_Button'] == '查看按钮':
            latesttime = time.ctime(os.path.getmtime('/home/test/WebTestTool/xuezhandaodi.out'))
            with open('/home/test/WebTestTool/xuezhandaodi.out', 'r', encoding='utf8') as f:
                a = f.readlines()
                resultControl = []
                test_result1 = ''
                test_result2 = ''
                timedata = str(request.form['time'])
                for i in a:
                    key = 'resultControl'
                    if key in i and timedata in i:
                        resultControl.append(i)
                cardtype = {'DuiDuiHu': '对对胡', 'QingYiSe': '清一色', 'XiaoQiDui': '小七对',
                            'LongQiDui': '龙七对', 'QingDui': '清对',
                            'JiangDui': '将对', 'QingQiDui': '清七对', 'JiangQiDui': '将七对', 'QingLongQiDui': '清龙七对',
                            'ShiBaLuoHan': '十八罗汉',
                            'QingShiBaLuoHan': '清十八罗汉', 'JiangJinGouDiao': '将金钩钓', 'QingJinGouDiao': '清金钩钩',
                            'QingYaoJiu': '清幺九',
                            'CT_NONE': '无叫', 'DianGang': '点杠', 'BaGang': '巴杠', 'AnGang': '暗杠', 'HuPai': '点炮',
                            'Zimo': '自摸', 'ChaDaJiao': '查大叫',
                            'Huazhu': '花猪', 'ServiceFee': '服务费', 'ZhuanYu': '转雨', 'GangShangKaiHua': '杠上开花',
                            'GangShangPao': '杠上炮',
                            'QiangGangHu': '抢杠胡', 'HaiDiLaoYue': '海底捞月', 'JinGouDiao': '金钩钩', 'TianHu': '天胡',
                            'DiHu': '地胡', 'RenHu': '人胡',
                            'DuanYaoQiu': '断幺九', 'MengQing': '门清', 'DaiYaoJiu': '带幺九'}
                cardindex = 1
                for cardtypeid in cardtype:
                    for result in resultControl:
                        if cardtypeid in result:
                            a = 1
                            test_result1 += ''.join('牌型{}：{}  已覆盖\n'.format(cardindex, cardtype[cardtypeid]))
                            break
                    if a != 1:
                        test_result2 += ''.join('牌型{}：{}  未覆盖\n'.format(cardindex, cardtype[cardtypeid]))
                    a = 0
                    cardindex += 1
                return render_template('maj_TestCoverage.html', TestResult1=test_result1, TestResult2=test_result2, Time=timedata, LatestTime=latesttime)
    return render_template('maj_TestCoverage.html')


@app.route('/doudz_TestCoverage.html', methods=['GET', 'POST'])
def doudz_TestCoverage():
    if request.method == 'GET':
        if os.path.exists('/home/test//WebTestTool/doudizhu.out') is True:
            latesttime = time.ctime(os.path.getmtime('/home/test//WebTestTool/doudizhu.out'))
            return render_template('doudz_TestCoverage.html', LatestTime=latesttime)
    if request.method == 'POST':
        if request.form['Submit_Button'] == '下载日志':
            try:
                ser_url = paramiko.Transport('10.0.0.32', 22)
                ser_url.connect(username='testsvr', password='123456')
                sftp = paramiko.SFTPClient.from_transport(ser_url)
                sftp.get('/tmp/doudizhu.out', '/home/test/WebTestTool/doudizhu.out')
                latesttime = time.ctime(os.path.getmtime('/home/test/WebTestTool/doudizhu.out'))
                ser_url.close()
                return render_template('doudz_TestCoverage.html', Tips='下载成功', LatestTime=latesttime)
            except:
                return render_template('doudz_TestCoverage.html', Tips='下载失败')
        if request.form['Submit_Button'] == '查看按钮':
            latesttime = time.ctime(os.path.getmtime('/home/test/WebTestTool/doudizhu.out'))
            with open('/home/test/WebTestTool/doudizhu.out', 'r', encoding='utf8') as f:
                a = f.readlines()
                resultControl = []
                test_result1 = ''
                test_result2 = ''
                timedata = str(request.form['time'])
                for i in a:
                    key = ''
                    if key in i and timedata in i:
                        resultControl.append(i)
                cardtype = {'JiaoDZ': '叫地主', 'QiangDZ': '抢地主', 'XuanBeiShu': '选倍数', 'Put': '出牌', 'Zha': '炸',
                            'Pass': '过', 'PuTongJiaBei': '普通加倍', 'ChaojiJiaBei': '超级加倍', 'JiaoDizhuAddTimes': '叫地主加倍',
                            'QiangDizhuAddTimes': '抢地主加倍', 'BombAddTimes': '炸弹加倍', 'WangZhaAddTimes': '王炸加倍', 'RocketAddTimes': '火箭加倍',
                            'SpringAddTimes': '春天加倍', 'AntiSpringAddTimes': '反春天加倍', 'DizhuAddTimes': '地主加倍', 'BuJiaBei': '不加倍',
                            'DanPai': '单牌', 'DuiZi': '对子', 'SanZhang': '单三张', 'ZhaDan': '炸弹类型', 'HuoJian': '火箭类型', 'ShunZi': '顺子',
                            'LianDui': '连续对子', 'SanDaiYi': '三带一单', 'SanDaiDui': '三带一对', 'FeiJi': '飞机', 'FeiJiDaiDanChi': '飞机带单翅膀',
                            'FeiJiDaiShuang': '飞机带双翅膀', 'SiDaiDan': '四带两单', 'SiDaiDui': '四带两对', 'ServiceFee': '服务费'}
                cardindex = 1
                for cardtypeid in cardtype:
                    for result in resultControl:
                        if cardtypeid in result:
                            a = 1
                            test_result1 += ''.join('牌型{}：{}  已覆盖\n'.format(cardindex, cardtype[cardtypeid]))
                            break
                    if a != 1:
                        test_result2 += ''.join('牌型{}：{}  未覆盖\n'.format(cardindex, cardtype[cardtypeid]))
                    a = 0
                    cardindex += 1
                return render_template('doudz_TestCoverage.html', TestResult1=test_result1, TestResult2=test_result2, Time=timedata, LatestTime=latesttime)
    return render_template('doudz_TestCoverage.html')


@app.route('/checkconfig.html', methods=['GET', 'POST'])
def checkconfig():
    if request.method == 'POST':
        checkresult = ''
        filelist = ['add_times_info_doudizhu.xlsx', 'game_config.xlsx', 'handcard_info.xlsx', 'person_aicontrol_info.xlsx',
                    'platform_group_control.xlsx', 'platform_person_control.xlsx', 'takecard_info.xlsx', 'type_score_xuezhan.xlsx', 'xuezhandaodi.xlsx']
        for filename in filelist:
            fileurl = r'E:\designer\配置表\{}'.format(filename)
            sheet = openxl(fileurl)
            xl_rows = sheet.nrows
            xl_rows -= 4
            try:
                for row in range(xl_rows):
                    sql = 'select * from {} where id={}'.format(filename[:-5], row+1)
                    sql_result = con_mysql(sql)
                    sql_result = list(sql_result)
                    xl_result = sheet.row_values(row+4)
                    for i in range(len(xl_result)):
                        if type(xl_result[i]) is float:
                            xl_result[i] = round(xl_result[i])
                        if sql_result[i] != xl_result[i] and type(sql_result[i]) == type(xl_result[i]):
                            result = '表名：{},第{}行,第{}列->ERROR! 配置表为：{} 数据库为：{} 表地址：{}\n'.format(filename, row+1, i+1, xl_result[i], sql_result[i], fileurl)
                            # result = result.ljust(150, ' ')
                            checkresult += result
            except:
                pass
        if len(checkresult) == 0:
            return render_template('checkconfig.html', CheckResult='恭喜！本次数据表检查没有发现差异！')
        return render_template('checkconfig.html', CheckResult=checkresult)
    return render_template('checkconfig.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
