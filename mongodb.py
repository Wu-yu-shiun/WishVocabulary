from pymongo.mongo_client import MongoClient

def get_user_data(user_id):
    uri = "mongodb+srv://vocab:nHKwiaM9WgcY28uG@mycluster.2jiwdws.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    userdata = client[user_id]
    return userdata

def get_oneday_data(user_id,date): 
    userdata = get_user_data(user_id)
    allword = userdata[date]
    return allword

def print_allword(data):
    cursor = data.find({})
    for doc in cursor:
        print(doc)

def add_word(data,id,english,chinese,pronunciation):
    result = data.insert_one({
        "id": id,
        "english": english,
        "chinese": chinese,
        "pronunciation": pronunciation,
    })
    print("資料新增成功!id="+str(result.inserted_id))

def delete_word(data,id):
    result=data.delete_one({"id":id})
    print("資料刪除成功!刪除了第"+str(id)+"筆資料")

def delete_allword(data):
    result=data.delete_many({})
    print("資料刪除成功!共刪除了"+str(result.deleted_count)+"筆資料")

def get_word(data,id):
    word=data.find_one({"id":id})
    return word

def get_word_id(user_id):
    userdata = get_user_data(user_id)
    data = userdata["word counter"]
    counter_record = data.find_one({})
    if counter_record and 'counter' in counter_record:
        new_counter = counter_record['counter'] + 1
        data.update_one({}, {'$set': {'counter': new_counter}})
        return new_counter
    else:
        data.insert_one({'counter': 1})
        return 1




# data=get_oneday_data("test","db_230630")
# for i in range(1, 8):
#     add_word(data,i,"ant","螞蟻","urlll")
# print_allword(data)
# delete_allword(data)
# delete_word(data,5)

# -------------------------------------------------------------

# uri = "mongodb+srv://vocab:nHKwiaM9WgcY28uG@mycluster.2jiwdws.mongodb.net/?retryWrites=true&w=majority"
# client = MongoClient(uri)
# collection=client["test"]["db_230629"]

# # 新增一筆
# # result=collection.insert_one({
# #     "number":99,
# #     "English":"eat",
# #     "Chinese":"吃",
# #     "pronunciation":"url",
# # })
# # print("資料新增成功!id="+str(result.inserted_id))

# 找全部
# cursor=collection.find({})
# for doc in cursor:
#     print(doc["english"])

# 找一筆
# from bson.objectid import ObjectId
# data=collection.find_one(ObjectId("649ce94c28109c2cc08cd812"))
# print(data["Chinese"])
# data=collection.find_one({"Chinese":"吃"})
# print(data)

# 更新多筆
# result=collection.update_many( {"English":"eat"} , {"$set":{"Chinese":"吃東西"}} )
# print(result.matched_count)
# print(result.modified_count)

# 刪除多筆
# result=collection.delete_many({"number":1})
# print(result.deleted_count)

# 刪除全部
# collection.delete_many({})

# 排序
# cursor=collection.find({},sort=[("number",pymongo.ASCENDING)])
# for doc in cursor:
#     print(doc)



