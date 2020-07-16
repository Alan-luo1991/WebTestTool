import requests,json
headers = {"Accept": "application/json, text/plain, */*",
           "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJrdWJvYXJkLXVzZXItdG9rZW4tYzJkOWoiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoia3Vib2FyZC11c2VyIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiZjMyYWU3MDQtYzU3OS0xMWVhLTllYTktMmU1NzJmMWJhNDgwIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmt1Ym9hcmQtdXNlciJ9.f5KhHVA8qgZz97k6ElmpBK2409hz5xi6ooD3repibczRxHmKX9k62q12kjarFRc00IbNpZf3-or2gUE-62FeW295m0cXd9bN4IAATC_K_LzPx4Aw9aY5i-204crz1aE_7rvazE5qBCFEBzMNfvtC9FMWOsOL-1BTug_du9C01PqLNjaAb5IBGqC1ZX1FWhultLRKnNfkdL1RhX2IvR6RwRhjUIKMvFCGFOx4tKbz0yOyJg-t8dSg7xlUvUhgW50ocLV63Cet8Am1oKGKzD2iK6ac-cclB6IR0gwNzujyYVklo4y6p1FMyXhcsJwZaqH0aCeBxgpJhj-7wlK5RHB7Zw",
           "Accept-Encoding": "gzip, deflate",
           "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
           "Cache-Control": "no-cache",
           "Connection": "keep-alive",
           "Cookie": "_ga=GA1.2.240738163.1594711187; _gid=GA1.2.341719617.1594711187; _gat=1",
           # "Host": "kuboard.xiaoxigua.top",
           # "Origin": "http://10.0.0.200:32567",
           # "Pragma": "no-cache",
           # "Referer": "http://kuboard.xiaoxigua.top/namespace/games/workload/upgrade",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"}
outernet_url = "http://kuboard.xiaoxigua.top/k8s-api/apis/apps/v1/namespaces/games/statefulsets?"
res_outernet = requests.get(outernet_url, headers=headers)


gatewaylist = ["gateway-payapi", "gateway-authapi", "gateway-lobbyapi", "gateway-xlch", "gateway-fkddz",
               "gateway-game-xzdd", "gateway-gameapi", "gateway-gwapi"]
for i in gatewaylist:
    updata_url = "http://kuboard.xiaoxigua.top/k8s-api/apis/apps/v1/namespaces/games/statefulsets/{}".format(i)
    get1 = requests.get(updata_url, headers=headers)
    try:
        jsondata = json.loads(get1.text)["metadata"]["resourceVersion"]
    except:
        pass
    print(jsondata)