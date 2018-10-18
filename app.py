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
    url_get = "https://tw.shop.com/"
    url_post = 'https://tw.shop.com/search/header'+event.message.text
    get_headers = {
        'Strict-Transport-Security':'max-age=63072000',
        'X-Akamai-Transformed':'9 - 0 pmb=mTOE,3',
        'Set-Cookie':'bm_mi=20FD1B4223293A37AC069EF503D09C85~KwiCkGrbYcrrljQBTQRDunSk8woRNrWDt4gvAMnioV5KClmV232P0rGEcbar1Jj92Jk5nAeiVD49qQr6jfk/6KeizRNikIHkXpphGhKnW3VMJG9ZU8mKWDBEBb4fxZSUR9quDF5Nv12CjvT/aZPxvlVbRe19b33eLIeeXRL74qeBb+xk/RMWb8jUdG9qxlxwVmK9RTCMU3dOnWd2RScHGQ==; Domain=.shop.com; Path=/; Max-Age=6521; HttpOnly',
        'Set-Cookie':'bm_sv=46127B2A4F99DE40CE6086289E3D0284~1iNajwGALBYwIChkVdis9WRqpN1sdoM5rMvddO4on+TI7BHxhQHQr7BLFEoA7NK14mJ9qOWxnzkCwSyQBPbuOkkNq4c7/A+18gRAW1WDguG/DSJmXHOKnOu8c5DUfhf8hzx3l/TcqqJ3+GrcfgDU8A==; Domain=.shop.com; Path=/; Max-Age=6531; HttpOnly'
    }
    get_data ={
        'COUNTRY_MATCH':'ture',
        'AMOS_OKTOCACHE':'false',
        'LAST_CCSYN_SRC':'FAMOS',
        'LAST_CCSYN':'13663',
        'CC_DISTID':'891059297',
        '_abck':'D4AAB695B1988CB5DFF906FAE8D7AC8517D2D7267F070000149BC85BC781872B~-1~fTMkdH1HnwlA0PZsQHApzW1kLXGOOMgYOIglnksTAnE=~-1~-1',
        'bm_sz':'D7702019F2ABC646C74E2EFB24FF4C67~QAAQJtfSF2t+13dmAQAAZcidh9UR6y3pDkfqIK591uzcB7VDKGnPdTnRCuFwpaGPoRypfZ3gcOEweCp7rNO7BNSFD17QuLTY6GssVJH6Z/g+yPPCN/NK55G0r3gXdT2mThAMH8ax43VCEX/dRb9kmjLvpwKxVI0npHwKvNwXmcy+c3CfQb+lfrjHFvWZ',
        'AMID':'3470255176',
        'CATALOGCITY_SSNLIVE13663':'3470255176',
        'CC_SRCID':'2791',
        'SHOPLOCAL_PROMO_SEEN':'0',
        'SHOPMF_NS_ID':'185',
        'PROMO_ACQUISITION_ELIGIBLE':'false',
        'ak_bmsc':'FC563E300622C1DBA5A339E61A78E83A8BAF57CEE12900001FC0C85BDB0BFC0F~plG+VKAud3YVZpDqJFava1893mES+0NF2coBXsSOXn1Qi5A2Wbb9Jn9DMqn8vA3JyvpidT+2lBa6IoEwp5i5kXWIFLs4fi1EkgGZDY6EkwiPa/19HzroQU7hM5nsiqkJnpZ06ELgLUtQU2SmbvlFrY8TXVqxMYJj/SkZ+YYBQsLI+UtAXrjb4+QLwcdsiaV4p/IOmjQqpvUgl1CbCSvJ1wGB6Tz6TakPGP9Jeh20UtDOI=',
        'bm_mi':'20FD1B4223293A37AC069EF503D09C85~KwiCkGrbYcrrljQBTQRDunSk8woRNrWDt4gvAMnioV5KClmV232P0rGEcbar1Jj92Jk5nAeiVD49qQr6jfk/6KeizRNikIHkXpphGhKnW3VMJG9ZU8mKWDBEBb4fxZSUR9quDF5Nv12CjvT/aZPxvlVbRe19b33eLIeeXRL74qeBb+xk/RMWb8jUdG9qxlxwVmK9RTCMU3dOnWd2RScHGQ==',
        'bm_sv':'46127B2A4F99DE40CE6086289E3D0284~1iNajwGALBYwIChkVdis9WRqpN1sdoM5rMvddO4on+TI7BHxhQHQr7BLFEoA7NK14mJ9qOWxnzkCwSyQBPbuOkkNq4c7/A+18gRAW1WDguG/DSJmXHOKnOu8c5DUfhf8hzx3l/TcqqJ3+GrcfgDU8A==',
        'JSESSIONID':'C985F3F68FA056A8DACE517A18A5260A',
        'CC_PORTALID':'1345008'
    }

    get_cookie = requests.get(url_get,data=get_data,headers=get_headers)
    print(get_cookie.text)
    soup_get = BeautifulSoup(get_cookie.text,'html.parser')
    print(get_cookie.status_code)

    siteID = soup_get.find(id='siteID')['value']
    countryCode = soup_get.find(id='countryCode')['value']
    countryCurrency = soup_get.find(id='countryCurrency')['value']
#    currency-template = soup_get.find(id='currency-template')['value']
    promoSetMenuId = soup_get.find(id='promoSetMenuId')['value']
    pageURL = soup_get.find(id='pageURL')['value']
    copyUrlDirections = soup_get.find(id='copyUrlDirections')['value']
#    service-site-url = soup_get.find(id='service-site-url')['value']
    data = {
        'st':'HTC',
        'sy':'product',
        'siteID':siteID,
        'countryCode':countryCode,
        'countryCurrency':countryCurrency,
        #'currency-template':currency-template,
        'promoSetMenuId':promoSetMenuId,
        'pageURL':pageURL,
        'copyUrlDirections':copyUrlDirections,

    }
    headers = {
        'referer':'https://tw.shop.com/',
        'Set-Cookie':'bm_mi=4DF817D9AA6A52D203AE7B7C771D88F1~1sMJHW9TcIHLUumH+Wq2QEWs16dq00CKeQ6XIPi0cYi9j/PWEpOQzDajd0hfHZABB9XAJ8nF8+ZTT0yyhFGHGbcatJXmvgJg7q21eHNanECaAXqqQ+71tLNA00xqStOu2SVrV3JL1iqTNC1matdxHNpJdviyu0pMlV0BXtRHDrkRyKaTTkymk3es+3T8od9WUJNsUVC1IHGu3A73cbKb1A==; Domain=.shop.com; Path=/; Max-Age=7111; HttpOnly',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'    
    }
    resp = requests.post(url_post,headers=headers,data=data,proxies={'https':'https://211.21.120.163:8080'})
    print(resp.status_code)
    resp_soup = BeautifulSoup(resp.text,'html.parser')
    price = resp_soup.find('div','product-results__final-price-m')
    print(price[0:10])
    line_bot_api.reply_message(event.reply_token, SentMassageText='It\'s work!')


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
