import requests
import json
import time
import random
import re

def check_updates():

    global TOKEN
    global offset
    global words

    URL = 'https://api.telegram.org/bot' # URL на который отправляется запрос

    data = {'offset': offset + 1, 'limit': 0, 'timeout': 0}

    try: # обрабатываем исключения
        request = requests.post(URL + TOKEN + '/getUpdates', data=data) # собственно сам запрос
        assert request.status_code == 200
    except:
        print('Error getting updates', request.request, request.text)
        return False

    if not request.status_code == 200: return False # проверяем пришедший статус ответа
    if not request.json()['ok']: return False

    for update in request.json()['result']:
        offset = update['update_id'] #  подтверждаем текущее обновление

        if 'message' not in update or 'text' not in update['message']: # это просто текст или какая-нибудь картиночка?
            print('Unknown message')
            continue



        getWord = 'Получить слово'
        count = 1
        text = ''

        if update['message']['text'].isdigit():
            count = min(int(update['message']['text']), 10)

        for i in range(count):
            text += words[random.randint(0,len(words)-1)]

        message_data = { # формируем информацию для отправки сообщения
            'chat_id': update['message']['chat']['id'], # куда отправляем сообщение
            'text': text, # само сообщение для отправки
            'reply_markup': {'keyboard': [[{'text': 'Получить слово'}], [{'text': '5'}, {'text': '10'}]]},
            # 'reply_to_message_id': update['message']['message_id'], # если параметр указан, то бот отправит сообщение в reply
            'parse_mode': 'HTML' # про форматирование текста ниже
        }

        try:
            request = requests.post(URL + TOKEN + '/sendMessage', json=message_data) # запрос на отправку сообщения
            assert request.status_code == 200
        except:
            print('Send message error:', request.request, request.text)
            return False

        if not request.status_code == 200: # проверим статус пришедшего ответа
            return False

with open('.token', 'r') as t:
    TOKEN=re.sub('^\s+|\n|\r|\s+$','', t.read())

with open('words', 'r') as f:
	words=f.readlines()

offset = 0

while True:
    try:
        check_updates()
        time.sleep(5)
    except KeyboardInterrupt: # порождается, если бота остановил пользователь
        print('Interrupted by the user')
        break
