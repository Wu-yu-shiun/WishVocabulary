import json

original_json = '''
{
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "填入日期",
        "weight": "bold",
        "size": "md"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "輸入英文",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 3,
                "margin": "md",
                "weight": "regular",
                "align": "start"
              },
              {
                "type": "text",
                "text": "輸入中文",
                "wrap": true,
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
        ]
      }
    ]
  }
}
'''

# # 模拟从 MongoDB 中获取当日单词的过程
# # 这里使用一个示例的单词列表
# word_list = [
#     {"english": "apple", "chinese": "蘋果"},
#     {"english": "banana", "chinese": "香蕉"},
#     {"english": "cat", "chinese": "貓"},
# ]

# # 将原始 JSON 字符串解析为 Python 字典
# json_data = json.loads(original_json)

# # 获取 "contents" 部分的内容
# contents = json_data["body"]["contents"]

# # 清空原始的 "contents" 部分内容
# contents.clear()

# # 添加日期信息到 "contents" 部分
# today = "填入日期"
# contents.append({
#     "type": "text",
#     "text": today,
#     "weight": "bold",
#     "size": "md"
# })

# # 根据单词列表生成对应的 JSON 内容并添加到 "contents" 部分
# for word in word_list:
#     english_word = word["english"]
#     chinese_word = word["chinese"]

#     word_content = {
#         "type": "box",
#         "layout": "baseline",
#         "spacing": "sm",
#         "contents": [
#             {
#                 "type": "text",
#                 "text": english_word,
#                 "color": "#aaaaaa",
#                 "size": "sm",
#                 "flex": 3,
#                 "margin": "md",
#                 "weight": "regular",
#                 "align": "start"
#             },
#             {
#                 "type": "text",
#                 "text": chinese_word,
#                 "wrap": True,
#                 "color": "#666666",
#                 "size": "sm",
#                 "flex": 2,
#                 "margin": "md"
#             }
#         ],
#         "borderWidth": "normal",
#         "borderColor": "#000000",
#         "margin": "none",
#         "height": "30px",
#         "paddingTop": "5px"
#     }

#     contents.append(word_content)

# # 将更新后的 JSON 内容转换回字符串形式
# updated_json = json.dumps(json_data)

# # 将更新后的 JSON 字符串保存到文件中
# with open("updated_json.json", "w") as file:
#     file.write(updated_json)
