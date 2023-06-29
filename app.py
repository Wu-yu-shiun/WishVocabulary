from flask import (Flask, request, abort)
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import os
import mongodb

# import configparser
# config = configparser.ConfigParser()
# config.read("config.ini")
# line_bot_api = LineBotApi(config['line_bot']['channel_access_token'])
# handler = WebhookHandler(config['line_bot']['channel_secret'])
# line_bot_api.push_message(config['line_bot']['my_user_id'], TextSendMessage(text='你可以開始了'))

# line_bot_api = LineBotApi('K/NEmvRBi3EfdNVOWUGxmBLXSkE9iIYjz2SXUHV7ioYLfD6FuZe+Y8J7GwSQSDW2kK04+p73qdK97Q1PhCScwN/KdHvSmQRrnIzuZCeIYeSqkhOUvSIQd5uIhetQkrKEbQAh6ZaZL5txW62L6axetAdB04t89/1O/w1cDnyilFU=')
# handler = WebhookHandler('cb25265c3668e1983601ae8c62705ea3')
# line_bot_api.push_message('Udb21c2cdfce57278db519a0b88153d82', TextSendMessage(text='系統有更新！'))

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
line_bot_api.push_message(os.getenv('MY_USER_ID'), TextSendMessage(text='系統有更新！'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    print("exe callback")
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
    msg=event.message.text
    profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_name
    user_id = profile.user_id
    print(msg,user_name,user_id)

    if msg == '[ 輸入單字 ]':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請開始輸入'))
        # 進入輸入模式
    elif  msg == '[ 查詢單字 ]':
        # 跳出要查詢的時間選項
        message=TextSendMessage(
            text='你要查詢哪一天？',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label="今日",text="查詢今日單字")),
                    QuickReplyButton(action=MessageAction(label="昨日",text="查詢昨日單字")),
                    QuickReplyButton(action=MessageAction(label="全部",text="查詢全部單字")),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
        # 進入查詢模式
    elif  msg == '[ 我要測驗 ]':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='你要測驗的範圍是？'))
        # 跳出要考試的範圍選項
        # 進入測驗模式
    elif msg == 'db':
        data=mongodb.get_oneday_data("test","db_230629")
        mongodb.print(data)
    else :
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Error'))
    
    

#主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

 