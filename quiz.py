
import mongodb



# mongodb的[user_name][quiz]先清空，加入一個accuary統計答對＆答錯題數
# 將被選到範圍的word放進[user_name][quiz]，將word補上一個importance的key 
def word_to_pool(user_id, id_min, id_max):
    pass



# 挑選要考哪個id的單字的演算法
# 包括何時該結束測驗(easy:只考10個,medium:全部importance歸0,hard:連續對10個)
def choose_word_algo(mode):
    id = 0
    return id

# 取出要當考題的單字英文
def get_word(id):
    pass

# 判斷答案是否過關
# 沒過關的懲罰機制
def judge_answer(anwser):
    pass


# 統計正確率
def print_accuarcy():

    pass