import requests

url = 'http://wms.test.vevor.net/api/wms-asserts-service/controller-assertsContainer/front/insert'

headers = {
    'Authorization': 'Bearer 1ee6eec5-1494-47e5-9eb9-d6d31f01ff7d'
}

params = {
    'containerCode': "",
    'createdName': "",
    'status': "",
    'warehouseId': 1
}

while True:
    response = requests.post(url=url, headers=headers, json=params)

    re = response.json()

    print(re)
