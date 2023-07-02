import requests

def get_word_audio_url(word):
    api_key = "1ea8c1bb-30f9-46e3-8ac8-e2fcc34380c7"
    url = f"https://www.dictionaryapi.com/api/v3/references/learners/json/{word}?key={api_key}"
    response = requests.get(url)
    data = response.json()
    audio = data[0]['hwi']['prs'][0]['sound']['audio']
    audio_url = "https://media.merriam-webster.com/audio/prons/en/us/mp3/"+word[0].lower()+"/"+str(audio)+".mp3"
    return audio_url

# word = "Pig"
# audio_url = get_word_audio_url(word)
# print("单词的发音URL:", audio_url)

