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

headers = {"Content-Type": "application/json", "Authorization": "7136829"}


def getbox(num):
    data = {"id": 200101}
    sky = 0
    boxlist = []
    while num > 0:
        res = requests.post("http://10.0.0.204:32581/plus/lootTest", json=data, headers=headers)
        if len(res.text) == 5:
            sky += 1
        else:
            boxlist.append(json.loads(res.text)[0]["id"])
        num -= 1
    result = "未掉落次数：{} ----铜宝箱数量:{}  银宝箱数量:{}  金宝箱数量:{}".format(sky, boxlist.count(100211), boxlist.count(100212), boxlist.count(100213))
    return result


def openbox(num):
    data = {"id": 200003}
    itemlist = []
    while num > 0:
        res = requests.post("http://10.0.0.204:32581/plus/lootTest", json=data, headers=headers)
        res = json.loads(res.text)
        for i in res:
            itemlist.append(i)
        num -= 1
    result = "道具出现次数详情：\n" + "金币-2000：{}次 金币-4000：{}次 金币-6000：{}次\n".format(itemlist.count({'id': 800002, 'n': 2000}), itemlist.count({'id': 800002, 'n': 4000}), itemlist.count({'id': 800002, 'n': 6000})) \
             + "经验材料C-5个：{}次 经验材料C-7个：{}次 经验材料B-5个：{}次 经验材料B-7个：{}次 ".format(itemlist.count({'id': 100302, 'n': 5}), itemlist.count({'id': 100704, 'n': 7}), itemlist.count({'id': 100303, 'n': 5}), itemlist.count({'id': 100306, 'n': 7}))\
             + "经验材料A-5个：{}次 经验材料A-7个：{}次 经验材料S-5个：{}次 经验材料S-7个：{}次\n".format(itemlist.count({'id': 100702, 'n': 5}), itemlist.count({'id': 100708, 'n': 7}), itemlist.count({'id': 100703, 'n': 5}), itemlist.count({'id': 100710, 'n': 7})) \
             + "记牌器1次-4个：{}次 记牌器1次-6个：{}次 记牌器1天-1个：{}次\n".format(itemlist.count({'id': 100211, 'n': 4}), itemlist.count({'id': 100211, 'n': 6}), itemlist.count({'id': 100211, 'n': 1})) \
             + "钥匙-1个：{}次 超级加倍卡-4个：{}次 超级加倍卡-6个：{}次\n".format(itemlist.count({'id': 100101, 'n': 1}), itemlist.count({'id': 100301, 'n': 4}), itemlist.count({'id': 100301, 'n': 6})) \
             + "魂玉-1个：{}次 魂玉-2个：{}次 魂玉-3个：{}次\n".format(itemlist.count({'id': 800003, 'n': 1}), itemlist.count({'id': 800003, 'n': 2}), itemlist.count({'id': 800003, 'n': 3})) \
             + "向墨：{}次 舒怡：{}次 康莉：{}次 玉祥：{}次 若琳：{}次 元一：{}次\n".format(itemlist.count({'id': 200001, 'n': 1}), itemlist.count({'id': 200002, 'n': 1}), itemlist.count({'id': 200003, 'n': 1}), itemlist.count({'id': 200004, 'n': 1}), itemlist.count({'id': 200005, 'n': 1}), itemlist.count({'id': 200006, 'n': 1}))
    return result


if __name__ == "__main__":
    pass

