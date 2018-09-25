from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('295PO7c2FbLmq2jHznxmISTQciVcWy7DnEIArWCgSUKWPsorlKbbuRURYIYxWZYJXjlQ2Wj9Ik8nwuAz2qB2rc4EfKN56kdvBERkjx7F1OOPsjx8cdCNGhoLQtVfAR+TrFsuw73JsEKI2IA9gE719gdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('6baf8c3075c7c10d98b7f1d4afcf2146')

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
@handler.add(MessageEvent, message=(TextMessage, ImageMessage))
def handle_message(event):
#將收到的訊息上傳至Imgur空間
    if  isinstance(event.message, ImageMessage):
        ext = 'jpg'
        message_conent = line_bot_api.get_message_content(event.message.id)        
        

        callback = TemplateSendMessage(
          alt_text='Buttons template',
          template=ButtonsTemplate(
            thumbnail_image_url='https://pic.pimg.tw/annaivy/4ace1761e1831.jpg',
            title='褐飛蝨蟲害判別結果',
            text='危害等級：尚無資料',
            actions=[
            PostbackTemplateAction(
                label='有幾隻褐飛蝨?',
                text='我還不會計算',
                data='action=buy&itemid=2'
            ),
            MessageTemplateAction(
                label='建議用藥',
                text='農特寧'
            ),
            URITemplateAction(
                label='相關資訊',
                uri='https://n.yam.com/Article/20131016823426'
            )
        ]
    )
)
        line_bot_api.reply_message(event.reply_token, callback)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
