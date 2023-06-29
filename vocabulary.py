import nltk
import requests

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

def print_word_details(word):
    if is_english_word(word):
        print(translate_word(word))
    else:
        print("不是英文單字。")

# print_word_details("wish")



