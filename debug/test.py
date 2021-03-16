"""
_*_ coding: UTF-8 _*_
@Time      : 2021/3/10 13:17
@Author    : LiuXiaoQiang
@Site      : https://github.com/qq183727918
@File      : test.py
@Software  : PyCharm
"""
import requests

url = "http://gateway.test.wms.vevor.net/wms-outbound-orders-service/api-IOverseasOutboundService/outer/create"
i = 1
while True:
    i += 1
    print(i)
    a = 20210316100001

    payload = {
        "sourceSn": f"DPCD{a + i}",
        "sourceCreatedBy": "system",
        "sourceCreatedTime": "2021-03-16 22:59:00",
        "warehouse": 18,
        "expectedDeliveryTime": "2021-03-16 21:18:00",
        "name": "Ricardo Sotelo",
        "phoneNum": "+1 763-225-9463 ext. 07064",
        "address": "1341 GOLDENEAGLE DR",
        "postcode": "92879-0809",
        "country": "United States",
        "tenantId": "vevor",
        "transType": 1,
        "logisticsInfo": 5,
        "shipmentMethod": 0,
        "billNo": f"DUCD{a + i}",
        "billUrl": "http://qiniu-test.vevor.net/ceshi-1611579817871.png",
        "vos": [{
            "goodsSku": "97-02-1013QCXS001V0",
            "goodsName": "线束 97-02 1013汽车",
            "num": 1
        }]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.json())

    if i == 10:
        break

# 多品
# duopin = {
#         "sourceSn": f"DUCD{a + i}",
#         "sourceCreatedBy": "system",
#         "sourceCreatedTime": "2021-03-16 22:59:00",
#         "warehouse": 18,
#         "expectedDeliveryTime": "2021-03-16 21:18:00",
#         "name": "Ricardo Sotelo",
#         "phoneNum": "+1 763-225-9463 ext. 07064",
#         "address": "1341 GOLDENEAGLE DR",
#         "postcode": "92879-0809",
#         "country": "United States",
#         "tenantId": "vevor",
#         "transType": 2,
#         "logisticsInfo": 5,
#         "shipmentMethod": 2,
#         "billNo": "DPCD20210316100001",
#         "billUrl": "http://qiniu-test.vevor.net/ceshi-1611579817871.png",
#         "vos": [{
#             "goodsSku": "DG2000LBSHSYTDQ01V0",
#             "goodsName": "吊钩 2000 lbs 黑色油桶吊钳",
#             "num": 10
#         }, {
#             "goodsSku": "QDJTSYYB000000001V0",
#             "goodsName": "气动脚踏式液压泵",
#             "num": 10
#         }]
#     }
# 大件
# dajian = {
#     "sourceSn": "DJCD20210316300001",
#     "sourceCreatedBy": "system",
#     "sourceCreatedTime": "2021-03-16 22:59:00",
#     "warehouse": 18,
#     "expectedDeliveryTime": "2021-03-16 21:18:00",
#     "name": "Ricardo Sotelo",
#     "phoneNum": "+1 763-225-9463 ext. 07064",
#     "address": "1341 GOLDENEAGLE DR",
#     "postcode": "92879-0809",
#     "country": "United States",
#     "tenantId": "vevor",
#     "transType": 3,
#     "logisticsInfo": 5,
#     "shipmentMethod": 2,
#     "billNo": "DPCD20210316100001",
#     "billUrl": "http://qiniu-test.vevor.net/ceshi-1611579817871.png",
#     "vos": [{
#         "goodsSku": "97-02-1013QCXS001V0",
#         "goodsName": "线束 97-02 1013汽车",
#         "num": 10
#     }]
# }
