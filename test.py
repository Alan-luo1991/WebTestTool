import requests,json
login = requests.post("http://10.0.0.204:32581/agent/userAuthorize", json={"UserID": "OY4U6RUJ51MLF7K2", "UserName": ""}, headers={"Content-Type": "application/json"})
token = json.loads(login.text)['token']
header1 = {"Content-Type": "application/json", "Authorization": token}
data = {"storeType": 1, "goodsId": 10389401}
roleFight = requests.post("http://10.0.0.204:32581/mall/buy", json=data, headers=header1)
print(roleFight.text)

