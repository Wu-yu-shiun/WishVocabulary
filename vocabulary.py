import nltk
import requests
import re

def is_english_word(word):
    nltk.download('words')
    english_words = set(nltk.corpus.words.words())
    if word.lower() in english_words:
        return True
    return False

def translate_word(word):
    # 使用Google Translate API翻譯英文單字為中文
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {
        "key": "AIzaSyBfYJUeCEpIYFsrKDjZIaYRHNbnoRDKru8",
        "q": word,
        "source": "en",
        "target": "zh-TW"
    }
    response = requests.get(url, params=params)
    translation = response.json()["data"]["translations"][0]["translatedText"]
    return translation

def deal_word(word):
    if is_english_word(word):
        return translate_word(word)
    else:
        return None

def is_chinese_word(text):
    pattern = r'^[\u4e00-\u9fff]+$'  # 中文Unicode範圍
    return bool(re.match(pattern, text))

# print_word_details("wish")



