import json
import mongodb

def write_flex_message(user_id, date):
    with open('flex_message_module.json', 'r') as file: #  開啟flex_message.json檔
        template = json.load(file)

    template['body']['contents'][0]['text'] = date  # 標題改為日期
    print("標題改為日期ok")

    word_list=mongodb.get_oneday_data(user_id, date).find({}) # 取得當日資料

    contents = []
    for data in word_list:
        content = {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": data['english'],
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 3,
                    "margin": "md",
                    "weight": "regular",
                    "align": "start"
                },
                {
                    "type": "text",
                    "text": data['chinese'],
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 2,
                    "margin": "md"
                }
            ],
            "borderWidth": "normal",
            "borderColor": "#000000",
            "margin": "none",
            "height": "30px",
            "paddingTop": "5px"
        }
        contents.append(content)

    template['body']['contents'][1]['contents'] = contents # 更新模板中的内容

    json_data = json.dumps(template) # Python dic => json
    return json_data

