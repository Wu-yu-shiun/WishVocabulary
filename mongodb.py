from pymongo.mongo_client import MongoClient

def get_all_data(user_id):
    uri = "mongodb+srv://vocab:nHKwiaM9WgcY28uG@mycluster.2jiwdws.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    db = client[user_id]
    return db

def get_oneday_data(user_id,date): 
    print("get one data")
    db=get_all_data(user_id)
    datalist=db[date]
    return datalist

def print(data):
    cursor=data.find({"Chinese":"吃"})
    for doc in cursor:
        print(doc)

# def get_one_word(data,e):

def add_word(data,number,english,chinese,pronunciation):
    print("新增中")
    result=data.insert_one({
        "number":number,
        "english":english,
        "chinese":chinese,
        "pronunciation":pronunciation,
    })
    print("資料新增成功!id="+str(result.inserted_id))


# uri = "mongodb+srv://vocab:nHKwiaM9WgcY28uG@mycluster.2jiwdws.mongodb.net/?retryWrites=true&w=majority"
# client = MongoClient(uri)
# collection=client["test"]["db_230629"]

# 新增一筆
# result=collection.insert_one({
#     "number":99,
#     "English":"eat",
#     "Chinese":"吃",
#     "pronunciation":"url",
# })
# print("資料新增成功!id="+str(result.inserted_id))

# 找全部
# cursor=collection.find({"Chinese":"吃東西"})
# for doc in cursor:
#     print(doc["English"])

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



