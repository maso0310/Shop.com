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
    url_get = "https://tw.shop.com/maso0310"
    url_post = 'https://tw.shop.com/search/header'+event.message.text
    get_headers = {
        'accept-language':'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    get_data ={
        'COUNTRY_MATCH':'ture',
        'AMOS_OKTOCACHE':'false'
    }

    get_cookie = requests.get(url_get,data=get_data,headers=get_headers,proxies={'https':'https://59.127.187.73:44068'},timeout=3600)
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
    resp = requests.post(url_post,headers=headers,data=data,proxies={'https':'://59.127.187.73:44068'},timeout=3600)
    print(resp.status_code)
    resp_soup = BeautifulSoup(resp.text,'html.parser')
    price = resp_soup.find('div','product-results__final-price-m')
    print(price[0:10])
    line_bot_api.reply_message(event.reply_token, SentMassageText='It\'s work!')


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
