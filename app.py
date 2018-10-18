from flask import Flask, request, abort
import requests
import urllib3
import random
from bs4 import BeautifulSoup
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('TNwu7tqho7m8MnMSmG8jpAF8tWl+hzBQzb/JKdbDBJv3HkMAUJiz8uo0nS0hG89tbsjQk8IV02p/v5ChZ1txRKjMlvPufgBPak5Y5AEwJt84wc9Mocg+yeZ8oyRQcfwFKnfmNaNRJR27Qc9r6iY38AdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('d184dfc3ec38e22fb7edf6b7275023a8')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    url = 'https://tw.shop.com/search/header'
    data = {
        'st':event.message.text,
        'sy':'product'
    }
    headers = {
        'cookie':'_ga=GA1.2.378382800.1538583996; _abck=0AE15F4ADA3960F1AC0D2A4C7F1CE3958BAF57CEE1290000BAEDB45B6C21EA0B~0~Lq9sClEJ18HP4hmArd9dt6IPQbW/h88vjLh5DxKpHXk=~-1~-1; AMID=3461958957; _caid=5f0c7cd5-1d19-4777-8e66-628180d356a5; s_fid=349D6768623B1D1A-14A3E088EE11E193; s_vi=[CS]v1|2DDE57DE852A27EE-4000010640000557[CE]; s_getNewRepeat=1539093156329-New; LAST_CCSYN=13663; SPRING_SECURITY_REMEMBER_ME_COOKIE=YmFsaW1vbkBob3RtYWlsLmNvbTo5OTk5OTk5OTk5OTk5OmE3NmQ5ZjZiZmUzYTdlNDJjYTRhYTFlOTlhNWEwOTVh; CATALOGCITY_NCID=hXjVYZqzzqzUmzhUUVzqhpezmpYZxYVqYWZXzqwpk; CC_PORTALID=1345008; CC_DISTID=891059297; ENERGY_NCID=hXjVYZqzzqzUmzhUUVzqhpezmpYZxYVqYWZXzqwpk; JSESSIONID=4218E5A2B68B8D23B18DFE7EECBE0CD6; LAST_CCSYN_SRC=FAMOS; CATALOGCITY_SSNLIVE13663=3470231984; CC_SRCID=2791; SHOPLOCAL_PROMO_SEEN=0; AMOS_OKTOCACHE=false; COUNTRY_MATCH=true; SHOPMF_NS_ID=186; PROMO_ACQUISITION_ELIGIBLE=false; AKA_A2=A; bm_sz=88ED8867D52287A2A1E878274DB179EF~QAAQzleviwgrLjZmAQAAD4toh4M4VPihWhvDJAJirJj2Kr+wi/+e0VIwqkv/mHh11tEy5L+dXcnnA1jXCKN1iMfqkQL76ZvLvdKYXGRA/PYMGJc0FWF5nZfhUjsLpnuv16hAczqwNXAH1gx7eBoIsh9ba1YY08myecYw3LDGjqHEejiBuACPWMKqK5fD; utag_main=v_id:01663ac0a5b3000528ffcf35747703073001406b00739$_sn:5$_ss:1$_st:1539871869732$vapi_domain:shop.com$_pn:1%3Bexp-session$ses_id:1539870069732%3Bexp-session; _gid=GA1.2.1236809842.1539870070; AMCVS_127B38B3527845B30A490D4C%40AdobeOrg=1; AMCV_127B38B3527845B30A490D4C%40AdobeOrg=1099438348%7CMCIDTS%7C17823%7CMCMID%7C66624622681955232763002271045725787131%7CMCAAMLH-1539997644%7C11%7CMCAAMB-1540474869%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1539877269s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-17815%7CvVersion%7C2.1.0%7CMCCIDH%7C1295671552; mbox=PC#760aee998fef4f7b99fe53cda8a94204.22_1#1547646071|check#true#1539870130|session#9beb24fd2cbb4bab940e46038a89694e#1539871930; ak_bmsc=6C40C0C23983DB0D8F5DBD34EA6BC1AE8BAF57CEE1290000738DC85B0AF95952~plS1/X3/6jH/cvrqSZi7DgzK9B7O4+cXksyJ0Pq7Zvq4wCjfjX0FwOgcSifDyePrX6fA5BevV7Ly/h6pN1WqxLgBrSajYy5pVCJ3AlYiRN86jABYUXpGRgFXujVQt/XPSJqdMaEufG7A0pf2ANzJgCc17pPRKuCm91CUp9ypH65/SNkVmFXlBT+fMj6zTf0hsY7mUjLE05zJSUpDQMJj85N0C+5psQoHA2TQrJyrbgIK2q6qA/bC/nGvlpWfBzkCB0; AMOS_SID=_live_ticks%3D1539870071107%26live%3DOEZNLHxzw%252Eh~hWhzYqmYzqWkXzhemxzYYwqzhVWVZYXpkwVZzejxxj; AMOS_NS_ID=233; UrCapture=2343c0f7-ae71-de38-baac-e5fee93d41ea; bm_sv=D7EE85C36601A104C6919BB86D9567C5~1iNajwGALBYwIChkVdis9VOjL9FTPLpcV74sBGGs7NW0CQ2udU3Tn0veukiNy/3ZZaKpCBB/ZIEm/H+lC4rfH4TbZv7BIbTdzvzeZHMNOtrNfvBEYR/xIwhXc6tqy70KtP95DNH8GZFYvq3wynypog==; _gali=search-form',
        'referer':'https://tw.shop.com/',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'    
    }
    resp = requests.post(url,headers=headers,data=data,proxies={'https':'https://220.135.202.15:42669'})

    print(resp.status_code)

    line_bot_api.reply_message(event.reply_token, resp.text)


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
