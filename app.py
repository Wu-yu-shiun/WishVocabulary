from flask import (Flask, request, abort)
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from pymongo.mongo_client import MongoClient
import os, mongodb, vocabulary, nltk, requests, datetime, pytz, json

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
line_bot_api.push_message(os.getenv('MY_USER_ID'), TextSendMessage(text='系統已就緒！'))
mode = 0  # 0:一般模式  1.1:輸入英文模式 1.2:輸入中文模式 2:查詢模式  3:測驗模式
eng = ''
chi = ''

with open('flex_message.json', 'r') as f:
    flex_message_json = json.load(f)


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    global mode, chi, eng, id
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
    global mode, chi, eng, id
    msg=event.message.text
    profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_name
    user_id = profile.user_id
    print(msg,user_name,user_id)

    if mode == 0:
        if msg == '[ 輸入模式 ]':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='進入輸入模式，請開始輸入英文單字'))
            mode = 1.1 # 進入輸入模式    
        elif  msg == '[ 查詢模式 ]':
            # 跳出要查詢的時間選項
            message=TextSendMessage(
                text='你要查詢哪一天的內容？',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="今日",text="[ 查詢今日單字 ]")),
                        QuickReplyButton(action=MessageAction(label="昨日",text="[ 查詢昨日單字 ]")),
                        QuickReplyButton(action=MessageAction(label="全部",text="[ 查詢全部單字 ]")),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token,message)
            mode = 2 # 進入查詢模式
            print(mode)
        elif  msg == '[ 測驗模式 ]':
            # 跳出要考試的範圍選項
            message=TextSendMessage(
                text='你要測驗的範圍是？',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="今日",text="[ 測驗今日單字 ]")),
                        QuickReplyButton(action=MessageAction(label="最近3日",text="[ 測驗最近3日單字 ]")),
                        QuickReplyButton(action=MessageAction(label="全部",text="[ 測驗全部單字 ]")),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token,message)
            mode = 3 # 進入測驗模式
            print(mode)

    elif mode == 1.1:
        if msg == '[ 輸入模式 ]':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='結束輸入'))
            mode = 0 # 返回一般模式
        else:
            result=vocabulary.deal_word(msg)
            if result is None:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text='您的輸入並非英文單字'))
            else :
                message=TextSendMessage(
                    text='請輸入單字的中文',
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(action=MessageAction(label=result,text=result)),   
                        ]
                    )
                )
                line_bot_api.reply_message(event.reply_token,message)
                mode = 1.2
                eng=msg
                chi=result
                print(mode,eng,chi)

    elif mode == 1.2:
        if msg == '[ 輸入模式 ]':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='結束輸入'))
            mode = 0 # 返回一般模式
            print(mode)
        elif msg == '[ 是 ]':
            local_timezone = pytz.timezone('Asia/Taipei')
            local_date = datetime.datetime.now(local_timezone).date()
            data=mongodb.get_oneday_data(user_id,str(local_date))
            mongodb.add_word(data,mongodb.get_word_id(user_id),eng,chi,"urlll")
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='已成功輸入！請繼續輸入英文單字'))
            mode = 1.1
            eng = chi = ''
            print(mode,eng,chi)
        elif msg == '[ 否 ]':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請重新輸入單字的中文'))
        elif vocabulary.is_chinese_word(msg):
            chi = msg
            message = TemplateSendMessage(
                alt_text='確認按鈕',
                template=ConfirmTemplate(
                    text='將「'+eng+'」的中文設定為「'+chi+'」？',
                    actions=[
                        MessageTemplateAction(
                            label = '是',
                            text = '[ 是 ]',
                        ),
                        MessageTemplateAction(
                            label = '否',
                            text = '[ 否 ]',
                        ),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token,message)
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='您的輸入並非中文，請重新輸入'))
    
    elif mode == 2:
        if  msg == '[ 查詢模式 ]':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='結束查詢'))
            mode = 0 # 返回一般模式
            print(mode)
        elif msg == '[ 查詢今日單字 ]':
            flex_message = FlexSendMessage(alt_text='Flex Message', contents=flex_message_json)
            line_bot_api.reply_message(event.reply_token, flex_message)
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='mode2未完成'))
    
    elif mode == 3:
        if  msg == '[ 測驗模式 ]':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='結束測驗'))
            mode = 0 # 返回一般模式
            print(mode)
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='mode3未完成'))
    
    elif msg == 'wishhhh' :
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="test"))
        data=mongodb.get_oneday_data("test","db_230629")
        mongodb.add_word(data,55,"ant","螞蟻","urlll")
    
    else :
        pass
        

# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

 