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
import svn.remote
import pymongo
import data_function
import maj_function
import public_function
import doudz_function
import operations_server
import json


# 实例化，可视为固定格式
app = Flask(__name__)


def openxl(fileurl):
    tablename = xlrd.open_workbook(fileurl)
    tablename = tablename.sheet_by_index(0)
    return tablename


@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template('homepage.html')


# route()方法用于设定路由；类似spring路由配置
@app.route('/login.html', methods=['GET', 'POST'])
def hello_world():
    return render_template('login.html')


@app.route("/homepage.html", methods=['GET', 'POST'])
def homepage():

    return render_template('homepage.html')


@app.route("/operations_ser.html", methods=['GET', 'POST'])
def operations():
    if request.method == 'GET':
        return render_template('operations_ser.html', ser_status=operations_server.selectstatus())
    if request.method == 'POST':
        try:
            servername = request.form['environment']
            version = request.form['version_data']
            process = request.form['process']
            if request.form['Submit_Button'] == '关闭服务器':
                result = operations_server.stop(servername)
                return render_template('operations_ser.html', result=result, ser_status=operations_server.selectstatus())
            if request.form['Submit_Button'] == '启动服务器':
                result = operations_server.start(servername)
                return render_template('operations_ser.html', result=result, ser_status=operations_server.selectstatus())
            if request.form['Submit_Button'] == '确认部署':
                if version == '':
                    return render_template('operations_ser.html', result='版本号不能为空！')
                result = operations_server.updata(servername, version)
                return render_template('operations_ser.html', result=result, ser_status=operations_server.selectstatus())
            if request.form['Submit_Button'] == '重启进程':
                if request.form['process'] == 'svc-roomserver':
                    result = operations_server.reload(servername, process)
                    return render_template('operations_ser.html', result=result, ser_status=operations_server.selectstatus())
                if request.form['process'] == 'svc-payserver':
                    result = operations_server.reload(servername, process)
                    return render_template('operations_ser.html', result=result, ser_status=operations_server.selectstatus())
        except:
            pass
    return render_template('operations_ser.html')


@app.route('/XZmaj_extends.html', methods=['GET', 'POST'])
def XZmaj_extends():
    global player
    if request.method == 'GET':
        return render_template('XZmaj_extends.html', fieldresult=data_function.gamesiteinfo(120), IPresult=public_function.Ipstate(120))
    if request.method == 'POST':
        if request.form['Submit_Button'] == '确认发送':
            return maj_function.deploycard(120)
        if request.form['Submit_Button'] == '换三张':
            return maj_function.changecard(120)
        if request.form['Submit_Button'] == '修改金币':
            try:
                public_function.updatagold_mongo()
                return render_template('XZmaj_extends.html', Tips='修改金币成功', User_id=public_function.updatagold_mongo())
            except:
                return render_template('XZmaj_extends.html', Tips='请检查游戏ID或者是否连接到内网', User_id=public_function.updatagold_mongo())
        if request.form['Submit_Button'] == '拿牌':
            return maj_function.nextcard(120)
        if request.form['Submit_Button'] == '配置':
            return maj_function.lastcard(120, 'send')
        if request.form['Submit_Button'] == '重置':
            return maj_function.lastcard(120, 'reset')
        if request.form['Submit_Button'] == '确定修改':
            return public_function.Robotswitch(120)
    return render_template('XZmaj_extends.html')


@app.route('/XLmaj_extends.html', methods=['GET', 'POST'])
def XLmaj_extends():
    global player
    if request.method == 'GET':
        return render_template('XLmaj_extends.html', fieldresult=data_function.gamesiteinfo(119), IPresult=public_function.Ipstate(119))
    if request.method == 'POST':
        if request.form['Submit_Button'] == '确认发送':
            return maj_function.deploycard(119)
        if request.form['Submit_Button'] == '换三张':
            return maj_function.changecard(119)
        if request.form['Submit_Button'] == '修改金币':
            try:
                public_function.updatagold_mongo()
                return render_template('XLmaj_extends.html', Tips='修改金币成功', User_id=public_function.updatagold_mongo())
            except:
                return render_template('XLmaj_extends.html', Tips='请检查游戏ID或者是否连接到内网', User_id=public_function.updatagold_mongo())
        if request.form['Submit_Button'] == '拿牌':
            return maj_function.nextcard(119)
        if request.form['Submit_Button'] == '配置':
            return maj_function.lastcard(119, 'send')
        if request.form['Submit_Button'] == '重置':
            return maj_function.lastcard(119, 'reset')
        if request.form['Submit_Button'] == '确定修改':
            return public_function.Robotswitch(119)
    return render_template('XLmaj_extends.html')


@app.route('/HLdoudz_extends.html', methods=['GET', 'POST'])
def HLdoudz_extends():
    if request.method == 'GET':
        return render_template('HLdoudz_extends.html', IPresult=public_function.Ipstate(100))
    if request.method == 'POST':
        if request.form['Submit_Button'] == '确认发送':
            return doudz_function.deploycard(100)
        if request.form['Submit_Button'] == '修改金币':
            try:
                public_function.updatagold_mongo()
                return render_template('HLdoudz_extends.html', Tips='修改金币成功', User_id=public_function.updatagold_mongo())
            except:
                return render_template('HLdoudz_extends.html', Tips='请检查游戏ID或者是否连接到内网', User_id=public_function.updatagold_mongo())
        if request.form['Submit_Button'] == '重新加载':
            switch = request.form['ip']
            myclient = pymongo.MongoClient(host='10.0.0.251', port=27017)
            mydb = myclient['wanke']
            mycol = mydb['gamekind']
            myquery = {'gameType': 100, 'enabled': bool(2 > 1)}
            if switch == 'open':
                newvalue = {'$set': {'matchIp': bool(2 > 1)}}
                mycol.update_many(myquery, newvalue)
                requests.get('http://10.0.0.204:30016/user/updategame')
                return render_template('HLdoudz_extends.html', Tips='IP限制已打开，相同IP无法匹配成功')
            if switch == 'close':
                newvalue = {'$set': {'matchIp': bool(1 > 2)}}
                mycol.update_many(myquery, newvalue)
                requests.get('http://10.0.0.204:30016/user/updategame')
                return render_template('HLdoudz_extends.html', Tips='IP限制已关闭，相同IP可以匹配了')
    return render_template('HLdoudz_extends.html')


@app.route('/FKdoudz_extends.html', methods=['GET', 'POST'])
def FKdoudz_extends():
    if request.method == 'GET':
        return render_template('FKdoudz_extends.html', IPresult=public_function.Ipstate(118))
    if request.method == 'POST':
        if request.form['Submit_Button'] == '确认发送':
            return doudz_function.deploycard(118)
        if request.form['Submit_Button'] == '修改金币':
            try:
                public_function.updatagold_mongo()
                return render_template('FKdoudz_extends.html', Tips='修改金币成功', User_id=public_function.updatagold_mongo())
            except:
                return render_template('FKdoudz_extends.html', Tips='请检查游戏ID或者是否连接到内网', User_id=public_function.updatagold_mongo())
        if request.form['Submit_Button'] == '重新加载':
            switch = request.form['ip']
            myclient = pymongo.MongoClient(host='10.0.0.252', port=27017)
            mydb = myclient['wanke']
            mycol = mydb['gamekind']
            myquery = {'gameType': 118, 'enabled': bool(2 > 1)}
            if switch == 'open':
                newvalue = {'$set': {'matchIp': bool(2 > 1)}}
                mycol.update_many(myquery, newvalue)
                requests.get('http://10.0.0.204:30016/user/updategame')
                return render_template('FKdoudz_extends.html', Tips='IP限制已打开，相同IP无法匹配成功')
            if switch == 'close':
                newvalue = {'$set': {'matchIp': bool(1 > 2)}}
                mycol.update_many(myquery, newvalue)
                requests.get('http://10.0.0.204:30016/user/updategame')
                return render_template('FKdoudz_extends.html', Tips='IP限制已关闭，相同IP可以匹配了')
    return render_template('FKdoudz_extends.html')


@app.route('/XZmaj_TestCoverage.html', methods=['GET', 'POST'])
def XZmaj_TestCoverage():
    latesttime = ''
    if request.method == 'GET':
        if os.path.exists('/home/test/WebTestTool/xuezhandaodi.out') is True:
            latesttime = time.ctime(os.path.getmtime('/home/test/WebTestTool/xuezhandaodi.out'))
            return render_template('XZmaj_TestCoverage.html', LatestTime=latesttime)
    if request.method == 'POST':
        if request.form['Submit_Button'] == '下载日志':
            try:
                ser_url = paramiko.Transport('10.0.0.32', 22)
                ser_url.connect(username='testsvr', password='123456')
                sftp = paramiko.SFTPClient.from_transport(ser_url)
                sftp.get('/tmp/xuezhandaodi.out', '/home/test/WebTestTool/xuezhandaodi.out')
                latesttime = time.ctime(os.path.getmtime('/home/test/WebTestTool/xuezhandaodi.out'))
                ser_url.close()
                return render_template('XZmaj_TestCoverage.html', Tips='下载成功', LatestTime=latesttime)
            except:
                return render_template('XZmaj_TestCoverage.html', Tips='下载失败')
        if request.form['Submit_Button'] == '查看按钮':
            if os.path.exists('/home/test/WebTestTool/xuezhandaodi.out') is True:
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
                    return render_template('XZmaj_TestCoverage.html', TestResult1=test_result1, TestResult2=test_result2, Time=timedata, LatestTime=latesttime)
    return render_template('XZmaj_TestCoverage.html')


@app.route('/HLdoudz_TestCoverage.html', methods=['GET', 'POST'])
def HLdoudz_TestCoverage():
    latesttime = ''
    if request.method == 'GET':
        if os.path.exists('/home/test/WebTestTool/stdout') is True:
            latesttime = time.ctime(os.path.getmtime('/home/test/WebTestTool/stdout'))
            return render_template('HLdoudz_TestCoverage.html', LatestTime=latesttime)
    if request.method == 'POST':
        if request.form['Submit_Button'] == '下载日志':
            try:
                logurl = request.form['logurl']
                ser_url = paramiko.Transport(logurl, 22)
                ser_url.connect(username='root', password='123456')
                sftp = paramiko.SFTPClient.from_transport(ser_url)
                sftp.get('/tmp/stdout', '/home/test/WebTestTool/stdout')
                latesttime = time.ctime(os.path.getmtime('/home/test/WebTestTool/stdout'))
                ser_url.close()
                return render_template('HLdoudz_TestCoverage.html', Tips='下载成功', LatestTime=latesttime)
            except:
                return render_template('HLdoudz_TestCoverage.html', Tips='下载失败')
        if request.form['Submit_Button'] == '查看按钮':
            if os.path.exists('/home/test//WebTestTool/stdout') is True:
                latesttime = time.ctime(os.path.getmtime('/home/test/WebTestTool/stdout'))
                with open('/home/test/WebTestTool/stdout', 'r', encoding='utf8') as f:
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
                    return render_template('HLdoudz_TestCoverage.html', TestResult1=test_result1, TestResult2=test_result2, Time=timedata, LatestTime=latesttime)
    return render_template('HLdoudz_TestCoverage.html')


@app.route('/checkconfig.html', methods=['GET', 'POST'])
def checkconfig():
    if request.method == 'POST':
        if request.form['checkconfig'] == '更新配置表':
            r = svn.remote.RemoteClient(r'https://10.0.0.22/svn/designer/配置表')
            r.checkout(r'/home/配置表')
        if request.form['checkconfig'] == '开始检查':
            checkresult = ''
            filelist = ['add_times_info_doudizhu.xlsx', 'game_config.xlsx', 'handcard_info.xlsx', 'person_aicontrol_info.xlsx',
                        'platform_group_control.xlsx', 'platform_person_control.xlsx', 'takecard_info.xlsx', 'type_score_xuezhan.xlsx', 'xuezhandaodi.xlsx']
            for filename in filelist:
                fileurl = r'/home/配置表/{}'.format(filename)
                sheet = openxl(fileurl)
                xl_rows = sheet.nrows
                xl_rows -= 4
                try:
                    for row in range(xl_rows):
                        sql = 'select * from {} where id={}'.format(filename[:-5], row+1)
                        sql_result = data_function.con_mysql(sql)
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
