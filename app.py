from flask import (Flask, request, abort)
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import os

# import configparser
# config = configparser.ConfigParser()
# config.read("config.ini")
# line_bot_api = LineBotApi(config['line_bot']['channel_access_token'])
# handler = WebhookHandler(config['line_bot']['channel_secret'])
# line_bot_api.push_message(config['line_bot']['my_user_id'], TextSendMessage(text='你可以開始了'))

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
line_bot_api.push_message(os.getenv('MY_USER_ID'), TextSendMessage(text='你可以開始了'))

# 監聽所有來自 / 的 Post Request
@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

# 訊息傳遞區塊

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)
    print(os.getenv('MY_USER_ID'))

#主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)