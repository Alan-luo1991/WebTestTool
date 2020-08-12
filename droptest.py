#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2020/8/7 下午 15:26
# @Author   : Alan_luo
# @Site     :
# @File     : WebTestTool.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c)  2019
# @Licence  :     <your licence>
# @Version  :   V1.0
import requests, json, time


def getheader(userid, url):
    login = requests.post(url + "/agent/userAuthorize", json={"UserID": userid, "UserName": userid},
                          headers={"Content-Type": "application/json"})
    token = json.loads(login.text)['token']
    header = {"Content-Type": "application/json", "Authorization": token}
    return header


def getbox(num, userid, url):
    data = {"id": 200101}
    if num == 0:
        result = "请输入正确的次数"
        return result
    a = num
    sky = 0
    boxlist = []
    while num > 0:
        res = requests.post(url + "/plus/lootTest", json=data, headers=getheader(userid, url))
        if len(res.text) == 5:
            sky += 1
        else:
            boxlist.append(json.loads(res.text)[0]["id"])
        num -= 1
    if (sky / a) * 100 == 0 or (sky / a) * 100 == 100:
        sky1 = str((sky / a) * 100)[:3] + "%"
    else:
        sky1 = str((sky / a) * 100)[:2] + "%"
    if a - sky == 0:
        box1, box2, box3 = "0.0%", "0.0%", "0.0%"
    else:
        if (boxlist.count(100211) / (a - sky)) * 100 < 10 or (boxlist.count(100211) / (a - sky)) * 100 == 100:
            box1 = str((boxlist.count(100211) / (a - sky)) * 100)[:3] + "%"
        else:
            box1 = str((boxlist.count(100211) / (a - sky)) * 100)[:2] + "%"
        if (boxlist.count(100212) / (a - sky)) * 100 < 10 or (boxlist.count(100212) / (a - sky)) * 100 == 100:
            box2 = str((boxlist.count(100212) / (a - sky)) * 100)[:3] + "%"
        else:
            box2 = str((boxlist.count(100212) / (a - sky)) * 100)[:2] + "%"
        if (boxlist.count(100213) / (a - sky)) * 100 < 10 or (boxlist.count(100213) / (a - sky)) * 100 == 100:
            box3 = str((boxlist.count(100213) / (a - sky)) * 100)[:3] + "%"
        else:
            box3 = str((boxlist.count(100213) / (a - sky)) * 100)[:2] + "%"
    result = "未掉落次数：{} 未掉落概率：{}\n铜宝箱数量: {}  掉落概率：{}\n银宝箱数量: {}  掉落概率：{}\n金宝箱数量: {}  掉落概率：{}\n".format(sky, sky1, boxlist.count(100211), box1, boxlist.count(100212), box2, boxlist.count(100213), box3)
    return result


def openbox(num, boxid, userid, url):
    data = {"id": boxid}
    itemlist = []
    while num > 0:
        res = requests.post(url + "/plus/lootTest", json=data, headers=getheader(userid, url))
        res = json.loads(res.text)
        for i in res:
            itemlist.append(i)
        num -= 1
    if boxid == 200001:
        result = "道具出现次数详情：\n" + "金币-500：{}次 金币-1000：{}次 金币-2000：{}次\n".format(
            itemlist.count({'id': 800002, 'n': 500}),
            itemlist.count({'id': 800002, 'n': 1000}),
            itemlist.count({'id': 800002, 'n': 2000})) \
                  + "经验材料C-1个：{}次 经验材料C-3个：{}次 经验材料B-1个：{}次 经验材料B-2个：{}次 ".format(
            itemlist.count({'id': 100707, 'n': 1}),
            itemlist.count({'id': 100714, 'n': 3}),
            itemlist.count({'id': 100702, 'n': 1}),
            itemlist.count({'id': 100710, 'n': 2})) \
                  + "经验材料A-1个：{}次 经验材料A-2个：{}次\n".format(itemlist.count({'id': 100711, 'n': 5}),
                                                         itemlist.count({'id': 100717, 'n': 7})) \
                  + "记牌器1次-2个：{}次 记牌器1次-4个：{}次 记牌器1次-7个：{}次\n".format(itemlist.count({'id': 100301, 'n': 2}),
                                                                      itemlist.count({'id': 100301, 'n': 4}),
                                                                      itemlist.count({'id': 100301, 'n': 7})) \
                  + "钥匙-1个：{}次 超级加倍卡-2个：{}次 超级加倍卡-4个：{}次\n".format(itemlist.count({'id': 100101, 'n': 1}),
                                                                   itemlist.count({'id': 100401, 'n': 2}),
                                                                   itemlist.count({'id': 100401, 'n': 4})) \
                  + "魂玉-1个：{}次 魂玉-2个：{}次 魂玉-3个：{}次\n".format(itemlist.count({'id': 800003, 'n': 1}),
                                                             itemlist.count({'id': 800003, 'n': 2}),
                                                             itemlist.count({'id': 800003, 'n': 3})) \
                  + "向墨：{}次 舒怡：{}次 康莉：{}次 玉祥：{}次 若琳：{}次 元一：{}次\n".format(itemlist.count({'id': 200001, 'n': 1}),
                                                                         itemlist.count({'id': 200002, 'n': 1}),
                                                                         itemlist.count({'id': 200003, 'n': 1}),
                                                                         itemlist.count({'id': 200004, 'n': 1}),
                                                                         itemlist.count({'id': 200005, 'n': 1}),
                                                                         itemlist.count({'id': 200006, 'n': 1}))
        return result
    if boxid == 200003:
        result = "道具出现次数详情：\n" + "金币-2000：{}次 金币-4000：{}次 金币-6000：{}次\n".format(itemlist.count({'id': 800002, 'n': 2000}), itemlist.count({'id': 800002, 'n': 4000}), itemlist.count({'id': 800002, 'n': 6000})) \
             + "经验材料C-5个：{}次 经验材料C-7个：{}次 经验材料B-5个：{}次 经验材料B-7个：{}次 ".format(itemlist.count({'id': 100714, 'n': 5}), itemlist.count({'id': 100707, 'n': 7}), itemlist.count({'id': 100708, 'n': 5}), itemlist.count({'id': 100709, 'n': 7}))\
             + "经验材料A-5个：{}次 经验材料A-7个：{}次 经验材料S-5个：{}次 经验材料S-7个：{}次\n".format(itemlist.count({'id': 100711, 'n': 5}), itemlist.count({'id': 100717, 'n': 7}), itemlist.count({'id': 100713, 'n': 5}), itemlist.count({'id': 100716, 'n': 7})) \
             + "记牌器1次-4个：{}次 记牌器1次-6个：{}次 记牌器1天-1个：{}次\n".format(itemlist.count({'id': 100301, 'n': 4}), itemlist.count({'id': 100301, 'n': 6}), itemlist.count({'id': 100302, 'n': 1})) \
             + "钥匙-1个：{}次 超级加倍卡-4个：{}次 超级加倍卡-6个：{}次\n".format(itemlist.count({'id': 100101, 'n': 1}), itemlist.count({'id': 100401, 'n': 4}), itemlist.count({'id': 100401, 'n': 6})) \
             + "魂玉-3个：{}次 魂玉-4个：{}次 魂玉-5个：{}次\n".format(itemlist.count({'id': 800003, 'n': 3}), itemlist.count({'id': 800003, 'n': 4}), itemlist.count({'id': 800003, 'n': 5})) \
             + "向墨：{}次 舒怡：{}次 康莉：{}次 玉祥：{}次 若琳：{}次 元一：{}次\n".format(itemlist.count({'id': 200001, 'n': 1}), itemlist.count({'id': 200002, 'n': 1}), itemlist.count({'id': 200003, 'n': 1}), itemlist.count({'id': 200004, 'n': 1}), itemlist.count({'id': 200005, 'n': 1}), itemlist.count({'id': 200006, 'n': 1}))
        return result


def usebox(num, userid, url):
    playerinfo = requests.post(url + '/plus/playerInfo', headers=getheader(userid, url))
    if json.loads(playerinfo.text)['diamonds'] < 10000:
        res_buyM = requests.post(url + '/mall/buy', json={"storeType": 2, "goodsId": 103897089},
                                 headers=getheader(userid, url))  # 买钻石5000个
    items = json.loads(playerinfo.text)['bg']['Items']
    boxindex = []
    for i, k in enumerate(items):
        if k is None:
            continue
        if k['MetaId'] == 100203:
            boxindex.append(i)
    if len(boxindex) == 0:
        a = 10
        while a > 0:
            res_buybox = requests.post(url + '/mall/buy', json={"storeType": 3, "goodsId": 103902464},
                                   headers=getheader(userid, url))  # 买金宝箱10个
            a -= 1
    itemlist = []
    while num > 0:
        res_set = requests.post(url + '/plus/StOpBox', json={"B1Idx": boxindex[0], "B2Idx": 1}, headers=getheader(userid, url))  # 放入宝箱
        res_open = requests.post(url + '/plus/UseBoxByDMD', json={"idx": 1, "diamond": 24}, headers=getheader(userid, url))
        res_open = json.loads(res_open.text)
        for i in res_open:
            itemlist.append(i)
        num -= 1
    result = "道具出现次数详情：\n" + "金币-500：{}次 金币-1000：{}次 金币-2000：{}次\n".format(itemlist.count({'id': 800002, 'n': 500}),
                                                                            itemlist.count({'id': 800002, 'n': 1000}),
                                                                            itemlist.count({'id': 800002, 'n': 2000})) \
              + "经验材料C-1个：{}次 经验材料C-3个：{}次 经验材料B-1个：{}次 经验材料B-2个：{}次 ".format(itemlist.count({'id': 100707, 'n': 1}),
                                                                              itemlist.count({'id': 100714, 'n': 3}),
                                                                              itemlist.count({'id': 100702, 'n': 1}),
                                                                              itemlist.count({'id': 100710, 'n': 2})) \
              + "经验材料A-1个：{}次 经验材料A-2个：{}次\n".format(itemlist.count({'id': 100711, 'n': 5}),
                                                     itemlist.count({'id': 100717, 'n': 7})) \
              + "记牌器1次-2个：{}次 记牌器1次-4个：{}次 记牌器1次-7个：{}次\n".format(itemlist.count({'id': 100301, 'n': 2}),
                                                                  itemlist.count({'id': 100301, 'n': 4}),
                                                                  itemlist.count({'id': 100301, 'n': 7})) \
              + "钥匙-1个：{}次 超级加倍卡-2个：{}次 超级加倍卡-4个：{}次\n".format(itemlist.count({'id': 100101, 'n': 1}),
                                                               itemlist.count({'id': 100401, 'n': 2}),
                                                               itemlist.count({'id': 100401, 'n': 4})) \
              + "魂玉-1个：{}次 魂玉-2个：{}次 魂玉-3个：{}次\n".format(itemlist.count({'id': 800003, 'n': 1}),
                                                         itemlist.count({'id': 800003, 'n': 2}),
                                                         itemlist.count({'id': 800003, 'n': 3})) \
              + "向墨：{}次 舒怡：{}次 康莉：{}次 玉祥：{}次 若琳：{}次 元一：{}次\n".format(itemlist.count({'id': 200001, 'n': 1}),
                                                                     itemlist.count({'id': 200002, 'n': 1}),
                                                                     itemlist.count({'id': 200003, 'n': 1}),
                                                                     itemlist.count({'id': 200004, 'n': 1}),
                                                                     itemlist.count({'id': 200005, 'n': 1}),
                                                                     itemlist.count({'id': 200006, 'n': 1}))
    return


if __name__ == "__main__":
    userid = '3397142363329372'
    url = 'http://10.0.0.204:32581'
    getheader(userid, url)
    openbox(1)

