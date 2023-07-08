from flask import (Flask, request, abort)
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from pymongo.mongo_client import MongoClient
import os, datetime, pytz, json, re
import mongodb, vocabulary, wordlist, pronounciation, quiz

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
line_bot_api.push_message(os.getenv('MY_USER_ID'), TextSendMessage(text='系統已被喚醒！'))
stage = 0  
eng = ''
chi = ''

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    global stage, chi, eng
    print("exe callback") ###
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
    global stage, chi, eng
    msg=event.message.text
    profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_name
    user_id = profile.user_id
    local_datetime = datetime.datetime.now(pytz.timezone('Asia/Taipei'))
    print(msg, user_name, user_id, local_datetime) ###

    if stage == 0:
        if msg == '[ 輸入模式 ]':
            stage = jump_to_stage(event,1.1,'進入輸入模式，請開始輸入英文單字(若想結束輸入，請再次在選單點選輸入)') # 進入輸入模式  
        elif  msg == '[ 查詢模式 ]':
            # 跳出要查詢的時間選項
            message=TextSendMessage(
                text='您要查詢哪一天的內容？',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="今天",text="[ 查詢今天單字 ]")),
                        QuickReplyButton(action=MessageAction(label="昨天",text="[ 查詢昨天單字 ]")),
                        QuickReplyButton(action=MessageAction(label="前天",text="[ 查詢前天單字 ]")),
                        QuickReplyButton(action=MessageAction(label="全部",text="[ 查詢全部單字 ]")),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token,message)
            stage = 2.1 # 進入查詢模式
            print(stage) ###
        elif  msg == '[ 測驗模式 ]':
            # 跳出要考試的範圍選項
            message=TextSendMessage(
                text='您要測驗的範圍是？',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="今天",text="[ 測驗今天單字 ]")),
                        QuickReplyButton(action=MessageAction(label="最近3天",text="[ 測驗最近3天單字 ]")),
                        QuickReplyButton(action=MessageAction(label="全部",text="[ 測驗全部單字 ]")),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token,message)
            stage = 3.1 # 選擇測驗模式
            print(stage) ###
        else:
            str1, str2 = split_pronounciation_command(msg)
            print(str1, str2) ###
            if ( vocabulary.is_english_word(str1) and str2 == '怎麼念' ):
                try:
                    url = pronounciation.get_word_audio_url(str1)
                    print(url) ###
                    message = AudioSendMessage(
                        original_content_url = url,
                        duration = 3000
                    )
                    line_bot_api.reply_message(event.reply_token, message)
                except:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="語音訊息取得失敗！"))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="查無指令，請從選單點選要進入的模式！"))

    elif stage == 1.1:
        if msg == '[ 輸入模式 ]':
            stage = jump_to_stage(event,0,'結束輸入')
        else:
            result=vocabulary.deal_word(msg)
            if result is None:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='您的輸入並非英文單字！'))
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
                stage = 1.2
                eng=msg
                chi=result
                print(stage,eng,chi) ###

    elif stage == 1.2:
        if msg == '[ 輸入模式 ]':
            stage = jump_to_stage(event,0,'結束輸入')
        elif msg == '[ 是 ]':
            data=mongodb.get_oneday_data(user_id,str(local_datetime.date()))
            mongodb.add_word(data,mongodb.get_word_id(user_id),eng,chi,"urlll")
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='已成功輸入！請繼續輸入英文單字(若想結束輸入，請再次在選單點選輸入)'))
            stage = 1.1
            eng = chi = ''
            print(stage,eng,chi) ###
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
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='您的輸入並非中文！請重新輸入'))
    
    elif stage == 2.1:
        if msg == '[ 查詢模式 ]':
            stage = jump_to_stage(event,0,'結束查詢')
        elif msg == '[ 查詢今天單字 ]':
            json_data = json.loads(wordlist.write_flex_message(user_id, str(local_datetime.date())))
            flex_message = FlexSendMessage(alt_text='Flex Message', contents=json_data)
            line_bot_api.reply_message(event.reply_token, flex_message)
            stage = 0
        elif msg == '[ 查詢昨天單字 ]':
            previous_datetime = local_datetime - datetime.timedelta(days=1)
            json_data = json.loads(wordlist.write_flex_message(user_id, str(previous_datetime.date())))
            flex_message = FlexSendMessage(alt_text='Flex Message', contents=json_data)
            line_bot_api.reply_message(event.reply_token, flex_message)
            stage = 0
        elif msg == '[ 查詢前天單字 ]':
            previous_datetime = local_datetime - datetime.timedelta(days=2)
            json_data = json.loads(wordlist.write_flex_message(user_id, str(previous_datetime.date())))
            flex_message = FlexSendMessage(alt_text='Flex Message', contents=json_data)
            line_bot_api.reply_message(event.reply_token, flex_message)
            stage = 0
        elif msg == '[ 查詢全部單字 ]':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='此功能未完成'))
            stage = 0  
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='您的輸入並非查詢指令！結束查詢'))
            stage = 0

    elif stage == 2.2:
        if  msg == '[ 查詢模式 ]':
            stage = jump_to_stage(event,0,'結束修改')
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='stage2.2未完成'))

    elif stage == 3.1:
        if  msg == '[ 測驗模式 ]':
            stage = jump_to_stage(event,0,'結束測驗')
        elif msg == '[ 測驗今天單字 ]':
            quiz.word_to_pool(user_id, 0, 5) #取id=0-5的單字到測驗池
            stage = choose_mode(event)
        elif msg == '[ 測驗最近3天單字 ]':
            quiz.word_to_pool(user_id, 0, 5) #取id=0-5的單字到測驗池
            stage = choose_mode(event)
        elif msg == '[ 測驗全部單字 ]':
            quiz.word_to_pool(user_id, 0, 5) #取id=0-5的單字到測驗池
            stage = choose_mode(event)
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='您的輸入並非測驗指令！結束測驗'))
            stage = 0

    elif stage == 3.2:
        if  msg == '[ 測驗模式 ]':
            stage = jump_to_stage(event,0,'結束測驗')
        elif msg == '[ 模式A ]':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='開始測驗模式A!'))
            stage = 3.31
        elif msg == '[ 模式B ]':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='開始測驗模式B!'))
            stage = 3.32
        elif msg == '[ 模式C ]':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='開始測驗模式C!'))
            stage = 3.33
        elif msg == '[ 模式D ]':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='開始測驗模式D!'))
            stage = 3.34
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='您的輸入並非測驗指令！結束測驗'))
            stage = 0

    elif stage == 3.31:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='stage3.31未完成'))
        stage = 0

    elif stage == 3.32:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='stage3.32未完成'))
        stage = 0

    elif stage == 3.33:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='stage3.33未完成'))
        stage = 0
        
    elif stage == 3.34:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='stage3.34未完成'))
        stage = 0
    
        
# 返回一般模式
def jump_to_stage(event,stage,str):
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=str))
    print(stage) ###
    return stage

# 切割發音指令
def split_pronounciation_command(str):
    matches = re.search(r"[^a-zA-Z]", str)  
    if matches:
        index = matches.start()  
        str1 = str[:index]  
        str2 = str[index:] 
    else:
        str1 = str 
        str2 = ""
    return str1, str2

# 選取要考的方式
def choose_mode(event):
    message=TextSendMessage(
        text='您要測驗的模式是？\n模式A:依序考完\n模式B:隨機考10個\n模式C:隨機考10個+錯過的要答對才結束\n模式D:連續對5個才結束',
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="模式A",text="[ 模式A ]")),
                QuickReplyButton(action=MessageAction(label="模式B",text="[ 模式B ]")),
                QuickReplyButton(action=MessageAction(label="模式C",text="[ 模式C ]")),
                QuickReplyButton(action=MessageAction(label="模式D",text="[ 模式D ]")),
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token,message)
    print(3.2) ###
    return 3.2

# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

 