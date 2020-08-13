#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2020/07/7 上午 11:26
# @Author   : Alan_luo
# @Site     :
# @File     : WebTestTool.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c)  2020
# @Licence  :     <your licence>
# @Version  :   V1.0 2020/07/09 16:21
import requests
import time
import json

lan_headers = {"Accept": "application/json, text/plain, */*",
               "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJrdWJvYXJkLXVzZXItdG9rZW4tZndsc2QiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoia3Vib2FyZC11c2VyIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiNzdjZTE5NmYtMjljYy00NWExLWI4NGQtNzM1Zjc0NGM0ZDJmIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmt1Ym9hcmQtdXNlciJ9.k3A7nD3KRKVzBuMMJEKRzUE2PUUA3-lkJgB1-xip2qsto-Ohjx_XlAjjeNcaopD3NgVrTBGh2PpF6gGrdr_OEYhcpFzja_E-frWyIKnH8UcIWs486LMECM-BosXd1sqhsBQphTWQf-5EDdWDMMQbzlQko5yWGqbHwm5SXPlXt3waKZnRGGijB8JeQ0wiVj-aP2FHLclxoc7hMDp1vVoBSljYlCjzpGxewgrweqhBQYjUELTgvTlAGRXzC0qOj25yLrF8v1EOMkNBvYNGzPI1QFmsiv2OmnnTGGLRoM8cqPLusZyfjsdDXvZDL0E2bVL7MSi9e2q_7QLBn6kfWmDjXw",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
               "Cache-Control": "no-cache",
               "Connection": "keep-alive",
               "Content-Type": "application/json;charset=UTF-8",
               "Cookie": "_ga=GA1.1.1618796466.1590981349; _gid=GA1.1.1039088035.1594018366; _gat=1",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"}

outernet_headers = {"Accept": "application/json, text/plain, */*",
                    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJrdWJvYXJkLXVzZXItdG9rZW4tYzJkOWoiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoia3Vib2FyZC11c2VyIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiZjMyYWU3MDQtYzU3OS0xMWVhLTllYTktMmU1NzJmMWJhNDgwIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmt1Ym9hcmQtdXNlciJ9.f5KhHVA8qgZz97k6ElmpBK2409hz5xi6ooD3repibczRxHmKX9k62q12kjarFRc00IbNpZf3-or2gUE-62FeW295m0cXd9bN4IAATC_K_LzPx4Aw9aY5i-204crz1aE_7rvazE5qBCFEBzMNfvtC9FMWOsOL-1BTug_du9C01PqLNjaAb5IBGqC1ZX1FWhultLRKnNfkdL1RhX2IvR6RwRhjUIKMvFCGFOx4tKbz0yOyJg-t8dSg7xlUvUhgW50ocLV63Cet8Am1oKGKzD2iK6ac-cclB6IR0gwNzujyYVklo4y6p1FMyXhcsJwZaqH0aCeBxgpJhj-7wlK5RHB7Zw",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Cookie": "_ga=GA1.2.240738163.1594711187; _gid=GA1.2.341719617.1594711187; _gat=1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"}

get_headers = {"Accept": "application/json, text/plain, */*",
               "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJrdWJvYXJkLXVzZXItdG9rZW4tZndsc2QiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoia3Vib2FyZC11c2VyIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiNzdjZTE5NmYtMjljYy00NWExLWI4NGQtNzM1Zjc0NGM0ZDJmIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmt1Ym9hcmQtdXNlciJ9.k3A7nD3KRKVzBuMMJEKRzUE2PUUA3-lkJgB1-xip2qsto-Ohjx_XlAjjeNcaopD3NgVrTBGh2PpF6gGrdr_OEYhcpFzja_E-frWyIKnH8UcIWs486LMECM-BosXd1sqhsBQphTWQf-5EDdWDMMQbzlQko5yWGqbHwm5SXPlXt3waKZnRGGijB8JeQ0wiVj-aP2FHLclxoc7hMDp1vVoBSljYlCjzpGxewgrweqhBQYjUELTgvTlAGRXzC0qOj25yLrF8v1EOMkNBvYNGzPI1QFmsiv2OmnnTGGLRoM8cqPLusZyfjsdDXvZDL0E2bVL7MSi9e2q_7QLBn6kfWmDjXw",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
               "Cache-Control": "no-cache",
               "Connection": "keep-alive",
               "Content-Type": "application/json;charset=UTF-8",
               "Cookie": "_ga=GA1.1.1618796466.1590981349; _gid=GA1.1.1039088035.1594018366; _gat=1",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"}
processlist = ["svc-roomserver", "svc-playerserver", "svc-payserver", "svc-agentserver", "gateway-payapi",
               "gateway-authapi", "gateway-lobbyapi", "gateway-xlch", "gateway-fkddz", "gateway-xzmj",
               "gateway-gameapi", "gateway-gwapi"]

gatewaylist = ["gateway-payapi", "gateway-authapi", "gateway-lobbyapi", "gateway-xlch", "gateway-fkddz", "gateway-xzmj",
               "gateway-gameapi", "gateway-gwapi"]

svclist = ["svc-roomserver", "svc-playerserver", "svc-payserver", "svc-agentserver"]

gatewaydict = {"gateway-payapi": "game-payapi", "gateway-authapi": "game-authapi", "gateway-lobbyapi": "game-lobbyapi",
               "gateway-xlch": "game-gameapi-xlch", "gateway-fkddz": "game-gameapi-fkddz", "gateway-xzmj": "game-gameapi-xzmj",
               "gateway-gameapi": "game-gameapi", "gateway-gwapi": "game-gwapi"}


def updata(servername, version):
    result = ''
    for process in svclist:
        if servername == 'games':
            ser_version = "reg.xiaoxigua.top/game/game-{}:{}".format(process[4:], version)
            updata_url = "http://kuboard.xiaoxigua.top/k8s-api/apis/apps/v1/namespaces/{}/statefulsets/{}".format(servername,
                                                                                                         process)
            header = outernet_headers
        else:
            ser_version = "10.0.0.250/wanke/game-{}:{}".format(process[4:], version)
            updata_url = "http://10.0.0.200:32567/k8s-api/apis/apps/v1/namespaces/{}/statefulsets/{}".format(servername,
                                                                                                         process)
            header = lan_headers
        get_test = requests.get(updata_url, headers=header)
        jsondata = json.loads(get_test.text)["metadata"]
        svc_data = {"apiVersion": "apps/v1", "kind": "StatefulSet",
                    "metadata": {"namespace": servername, "name": process,
                                 "annotations": {"k8s.eip.work/workload": process,
                                                 "k8s.eip.work/ingress": "false", "k8s.eip.work/service": "none"},
                                 "labels": {"k8s.eip.work/layer": "svc", "k8s.eip.work/name": process},
                                 "resourceVersion": jsondata["resourceVersion"]}, "spec": {
                "selector": {"matchLabels": {"k8s.eip.work/layer": "svc", "k8s.eip.work/name": process}},
                "template": {
                    "metadata": {"labels": {"k8s.eip.work/layer": "svc", "k8s.eip.work/name": process}},
                    "spec": {"securityContext": {"seLinuxOptions": {}}, "imagePullSecrets": [{"name": "harbor"}],
                             "restartPolicy": "Always", "initContainers": [], "containers": [
                            {"image": ser_version, "imagePullPolicy": "Always",
                             "name": process[4:], "volumeMounts": [], "resources": {"limits": {}, "requests": {}},
                             "env": [], "envFrom": [{"configMapRef": {"name": "env"}}]}], "volumes": [],
                             "hostAliases": [{"ip": "10.0.0.206", "hostnames": ["mongo1", "mongo2", "mongo3"]}],
                             "terminationGracePeriodSeconds": 10}}, "replicas": 1, "volumeClaimTemplates": [],
                "serviceName": process}}
        time.sleep(5)
        res_updata = requests.put(updata_url, json=svc_data, headers=header)
        result += res_updata.text + '\n'
    for process in gatewaylist:
        if servername == 'games':
            ser_version = "reg.xiaoxigua.top/game/{}:{}".format(gatewaydict[process], version)
            updata_url = "http://kuboard.xiaoxigua.top/k8s-api/apis/apps/v1/namespaces/{}/statefulsets/{}".format(
                servername,
                process)
            header = outernet_headers
        else:
            updata_url = "http://10.0.0.200:32567/k8s-api/apis/apps/v1/namespaces/{}/statefulsets/{}".format(servername,
                                                                                                         process)
            ser_version = "10.0.0.250/wanke/{}:{}".format(gatewaydict[process], version)
            header = lan_headers
        get_test = requests.get(updata_url, headers=header)
        jsondata = json.loads(get_test.text)["metadata"]
        try:
            gateway_data = {"apiVersion": "apps/v1", "kind": "StatefulSet",
                            "metadata": {"namespace": servername, "name": process,
                                         "annotations": {"k8s.eip.work/workload": process,
                                                         "k8s.eip.work/ingress": "false",
                                                         "k8s.eip.work/service": "none"},
                                         "labels": {"k8s.eip.work/layer": "gateway", "k8s.eip.work/name": process},
                                         "resourceVersion": jsondata["resourceVersion"]}, "spec": {
                    "selector": {"matchLabels": {"k8s.eip.work/layer": "gateway", "k8s.eip.work/name": process}},
                    "template": {
                        "metadata": {"labels": {"k8s.eip.work/layer": "gateway", "k8s.eip.work/name": process}},
                        "spec": {"securityContext": {"seLinuxOptions": {}},
                                 "imagePullSecrets": [{"name": "harbor"}],
                                 "restartPolicy": "Always", "initContainers": [], "containers": [
                                {"image": ser_version, "imagePullPolicy": "Always",
                                 "name": process[8:], "volumeMounts": [], "resources": {"limits": {}, "requests": {}},
                                 "env": [], "envFrom": [{"configMapRef": {"name": "env"}}]}], "volumes": [],
                                 "hostAliases": [
                                     {"ip": "10.0.0.206", "hostnames": ["mongo1", "mongo2", "mongo3"]}],
                                 "terminationGracePeriodSeconds": 30}}, "replicas": 1, "volumeClaimTemplates": [],
                    "serviceName": process}}
        except:
            pass
        time.sleep(5)
        res_updata = requests.put(updata_url, json=gateway_data, headers=header)
        result += res_updata.text + '\n'
    if servername == 'games':
        get_test = requests.get(
            "http://kuboard.xiaoxigua.top/k8s-api/api/v1/namespaces/games/services/gateway-gwapi",
            headers=outernet_headers)
        jsondata = json.loads(get_test.text)["metadata"]
        gwapi = {"apiVersion": "v1", "kind": "Service",
                 "metadata": {"namespace": "games", "name": "gateway-gwapi",
                              "resourceVersion": jsondata["resourceVersion"],
                              "annotations": {"k8s.eip.work/workload": "gateway-gwapi"},
                              "labels": {"k8s.eip.work/layer": "gateway", "k8s.eip.work/name": "gateway-gwapi"}},
                 "spec": {"selector": {"k8s.eip.work/layer": "gateway", "k8s.eip.work/name": "gateway-gwapi"},
                          "type": "NodePort",
                          "ports": [
                              {"port": 80, "targetPort": 80, "protocol": "TCP", "name": "bj8bkh", "nodePort": 32299}],
                          "clusterIP": "172.21.6.236"}}
        res_gwapi = requests.put('http://kuboard.xiaoxigua.top/k8s-api/apis/apps/v1/namespaces/games/statefulsets/gateway-gwapi'.format(
            servername), json=gwapi, headers=outernet_headers)
        result += res_gwapi.text + '\n'
    else:
        get_test = requests.get("http://10.0.0.200:32567/k8s-api/api/v1/namespaces/{}/services/gateway-gwapi".format(
            servername), headers=get_headers)
        jsondata = json.loads(get_test.text)["metadata"]
        gwapi = {"apiVersion": "v1", "kind": "Service",
                 "metadata": {"namespace": "wanda-test-use", "name": "gateway-gwapi",
                              "resourceVersion": jsondata["resourceVersion"],
                              "annotations": {"k8s.eip.work/workload": "gateway-gwapi"},
                              "labels": {"k8s.eip.work/layer": "gateway", "k8s.eip.work/name": "gateway-gwapi"}},
                 "spec": {"selector": {"k8s.eip.work/layer": "gateway", "k8s.eip.work/name": "gateway-gwapi"},
                          "type": "NodePort",
                          "ports": [{"port": 80, "targetPort": 80, "protocol": "TCP", "name": "bj8bkh", "nodePort": 32581}],
                          "clusterIP": "10.1.214.247"}}
        res_gwapi = requests.put('http://10.0.0.200:32567/k8s-api/api/v1/namespaces/{}/services/gateway-gwapi'.format(
            servername), json=gwapi, headers=lan_headers)
        result += res_gwapi.text + '\n'
    return result


def start(servername):
    result = ''
    for i in processlist:
        if servername == 'games':
            url = "http://kuboard.xiaoxigua.top/k8s-api/apis/apps/v1/namespaces/{}/statefulsets/{}/scale".format(
                servername, i)
            header = outernet_headers
        else:
            url = "http://10.0.0.200:32567/k8s-api/apis/apps/v1/namespaces/{}/statefulsets/{}/scale".format(servername,
                                                                                                            i)
            header = lan_headers
        data = {"kind": "Scale", "apiVersion": "autoscaling/v1", "metadata": {"namespace": servername, "name": i},
                "spec": {"replicas": 1}}
        time.sleep(3)
        res_start = requests.put(url, json=data, headers=header)
        result += res_start.text + "\n"
    return result


def stop(servername):
    result = ''
    for i in processlist:
        if servername == 'games':
            url = "http://kuboard.xiaoxigua.top/k8s-api/apis/apps/v1/namespaces/{}/statefulsets/{}/scale".format(
                servername, i)
            header = outernet_headers
        else:
            url = "http://10.0.0.200:32567/k8s-api/apis/apps/v1/namespaces/{}/statefulsets/{}/scale".format(servername,
                                                                                                            i)
            header = lan_headers
        data = {"kind": "Scale", "apiVersion": "autoscaling/v1", "metadata": {"namespace": servername, "name": i},
                "spec": {"replicas": 0}}
        time.sleep(3)
        res_stop = requests.put(url, json=data, headers=header)
        result += res_stop.text + "\n"
    return result


def reload(servername, process):
    if servername == 'games':
        url = "http://kuboard.xiaoxigua.top/k8s-api/api/v1/namespaces/{}/pods/{}-0".format(servername, process)
        header = outernet_headers
    else:
        url = "http://10.0.0.200:32567/k8s-api/api/v1/namespaces/{}/pods/{}-0".format(servername, process)
        header = lan_headers
    res_reload = requests.delete(url, headers=header)
    return res_reload.text


def selectstatus():
    test_url = "http://10.0.0.200:32567/k8s-api/apis/apps/v1/namespaces/wanda-test-use/statefulsets?"
    plan_url = "http://10.0.0.200:32567/k8s-api/apis/apps/v1/namespaces/wanda-ce-hua/statefulsets?"
    program_url = "http://10.0.0.200:32567/k8s-api/apis/apps/v1/namespaces/wanda-games/statefulsets?"
    # outernet_url = "http://kuboard.xiaoxigua.top/k8s-api/apis/apps/v1/namespaces/games/statefulsets?"
    res_test = requests.get(test_url, headers=lan_headers)
    res_plan = requests.get(plan_url, headers=lan_headers)
    res_program = requests.get(program_url, headers=lan_headers)
    # res_outernet = requests.get(outernet_url, headers=outernet_headers)
    test_result = json.loads(res_test.text)["items"][0]["spec"]["template"]["spec"]["containers"][0]["image"][-8:]
    plan_result = json.loads(res_plan.text)["items"][1]["spec"]["template"]["spec"]["containers"][0]["image"][-8:]
    program_result = json.loads(res_program.text)["items"][1]["spec"]["template"]["spec"]["containers"][0]["image"][-8:]
    # outernet_result = json.loads(res_outernet.text)["items"][1]["spec"]["template"]["spec"]["containers"][0]["image"][
    #                   -6:]
    server_status = "测试环境当前版本号：" + test_result + "\n" + "策划环境当前版本号：" + plan_result + "\n" + "开发环境当前版本号：" + program_result + "\n" + "外网测试环境当前版本号："
    return server_status


if __name__ == "__main__":
    print(selectstatus())