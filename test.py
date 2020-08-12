import requests,json
login = requests.post("http://10.0.0.204:32581/agent/userAuthorize", json={"UserID": "7136829", "UserName": ""}, headers={"Content-Type": "application/json"})
token = json.loads(login.text)['token']
print(token)
header1 = {"Content-Type": "application/json", "Authorization": token}
data = {"storeType": 1, "goodsId": 10389401}
roleFight = requests.post("http://10.0.0.204:32581/mall/buy", json=data, headers=header1)
print(roleFight.text)


