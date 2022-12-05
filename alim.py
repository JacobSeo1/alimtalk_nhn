import base64
import hashlib
import hmac
import time
import requests
import json
# import keys
# from filters import *


def send_message(phone):
    service_id = 1
    access_key = 2
    secret_key = 3

    url = "https://sens.apigw.ntruss.com"
    uri = "/alimtalk/v2/services/" + service_id + "/messages"
    api_url = url + uri
    timestamp = str(int(time.time() * 1000))
    access_key = access_key
    string_to_sign = "POST " + uri + "\n" + timestamp + "\n" + access_key
    signature = make_signature(string_to_sign)

    # 예약내역 불러와서 변환
    phone = send_message['phone'].replace("-", "")
    name = send_message['name']
    booking_date = format_datetime(send_message['date'])

    message = "{}님 bernini 예약이 승인되었습니다.\n예약일자: {}".format(name, booking_date)

    headers = {
        "Contenc-type": "application/json; charset=utf-8",
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": access_key,
        "x-ncp-apigw-signature-v2": signature,
      }

    body = {
        "plusFriendId": "string",
        "templateCode": "string",
        "messages":[
            {
                "countryCode":"string", #국가번호
                "to":user_phone_number.toString(), #수신자 번호
                "title":"string", #제목
                "content":"string", #내용
                # headerContent:"string"
                # itemHighlight:{
                #     title:"string",
                #     description:"string"
                # },
                # item:{
                #     list:[
                #         {
                #             title:"string",
                #             description:"string"
                #         }
                #     ],
                #     summary:{
                #         title:"string",
                #         description:"string"
                #     }
                # },
                # buttons:[
                #     {
                #         type:"string",
                #         name:"string",
                #         linkMobile:"string",
                #         linkPc:"string",
                #         schemeIos:"string",
                #         schemeAndroid:"string"
                #     }
                # ],
                
                # 전송에 실패했을 시 SMS로 전달
                # useSmsFailover: "boolean",
                # failoverConfig: {
                #     type: "string",
                #     from: "string",
                #     subject: "string",
                #     content: "string"
                # }
            }
        ],
        # reserveTime: "yyyy-MM-dd HH:mm", 메시지 발송 예약 일시 (yyyy-MM-dd HH:mm)
        # reserveTimeZone: "string", 예약 일시 타임존 (기본: Asia/Seoul)
        # scheduleCode: "string" 등록하려는 스케줄 코드
    }

    body = json.dumps(body)

    response = requests.post(api_url, headers=headers, data=body)
    response.raise_for_status()


def make_signature(string):
    secret_key = bytes(secret_key, 'UTF-8')
    string = bytes(string, 'UTF-8')
    string_hmac = hmac.new(secret_key, string, digestmod=hashlib.sha256).digest()
    string_base64 = base64.b64encode(string_hmac).decode('UTF-8')
    return string_base64