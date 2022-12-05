function send_message(phone) {
    var user_phone_number = phone;//수신 전화번호 기입
    var resultCode = 404;
    const date = Date.now().toString();
    const uri = process.env.SERVICE_ID; //서비스 ID
    const secretKey = process.env.NCP_SECRET_KEY;// Secret Key
    const accessKey = process.env.NCP_KEY;//Access Key
    const method = "POST";
    const space = " ";
    const newLine = "\n";
    const url = `https://sens.apigw.ntruss.com/alimtalk/v2/services/${uri}/messages`;
    const url2 = `/alimtalk/v2/services/${uri}/messages`;
    const hmac = CryptoJS.algo.HMAC.create(CryptoJS.algo.SHA256, secretKey);
    hmac.update(method);
    hmac.update(space);
    hmac.update(url2);
    hmac.update(newLine);
    hmac.update(date);
    hmac.update(newLine);
    hmac.update(accessKey);
    const hash = hmac.finalize();
    const signature = hash.toString(CryptoJS.enc.Base64);
    request({
      method: method,
      json: true,
      uri: url,
      headers: {
        "Contenc-type": "application/json; charset=utf-8",
        "x-ncp-apigw-timestamp": date,
        "x-ncp-iam-access-key": accessKey,
        "x-ncp-apigw-signature-v2": signature,
      },
      body: {
        plusFriendId:"string",
        templateCode:"string",
        messages:[
            {
                countryCode:"string", //국가번호
                to:user_phone_number.toString(), //수신자 번호
                title:"string", //제목
                content:"string", //내용
                // headerContent:"string"
                // itemHighlight:{
                //     title:"string",
                //     description:"string"
                // },
                // item:{
                //     list:[
                //         {
                //             title:"string",
                //             description:"string"
                //         }
                //     ],
                //     summary:{
                //         title:"string",
                //         description:"string"
                //     }
                // },
                // buttons:[
                //     {
                //         type:"string",
                //         name:"string",
                //         linkMobile:"string",
                //         linkPc:"string",
                //         schemeIos:"string",
                //         schemeAndroid:"string"
                //     }
                // ],
                
                // 전송에 실패했을 시 SMS로 전달
                // useSmsFailover: "boolean",
                // failoverConfig: {
                //     type: "string",
                //     from: "string",
                //     subject: "string",
                //     content: "string"
                // }
            }
        ],
        // reserveTime: "yyyy-MM-dd HH:mm", 메시지 발송 예약 일시 (yyyy-MM-dd HH:mm)
        // reserveTimeZone: "string", 예약 일시 타임존 (기본: Asia/Seoul)
        // scheduleCode: "string" 등록하려는 스케줄 코드
    },
    },
      function (err, res, html) {
        if (err) console.log(err);
        else { resultCode = 200; console.log(html); }
      }
    );
    return resultCode;
  }