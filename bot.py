"""Telegram bot."""
import requests
import time
import random
import re


def check_updates():
    """Telegram bot cycle."""
    global TOKEN
    global offset
    global words

    URL = 'https://api.telegram.org/bot'

    data = {'offset': offset + 1, 'limit': 0, 'timeout': 0}

    try:
        request = requests.post(URL + TOKEN + '/getUpdates', data=data)
        assert request.status_code == 200
    except:
        print('Error getting updates', request.request, request.text)
        return False

    if not request.status_code == 200:
        return False
    # проверяем пришедший статус ответа
    if not request.json()['ok']:
        return False

    for update in request.json()['result']:
        offset = update['update_id']

        if 'message' not in update or 'text' not in update['message']:
            print('Unknown message')
            continue

        getWord = 'Получить слово'
        count = 1
        text = ''

        if update['message']['text'].isdigit():
            count = min(int(update['message']['text']), 10)

        for i in range(count):
            text += words[random.randint(0, len(words) - 1)]

        message_data = {
            'chat_id': update['message']['chat']['id'],
            'text': text,
            'reply_markup': {'keyboard': [
                [{'text': getWord}], [{'text': '5'}, {'text': '10'}]
            ]},
            'parse_mode': 'HTML'
        }

        try:
            request = requests.post(
                URL + TOKEN + '/sendMessage',
                json=message_data
                )
            assert request.status_code == 200
        except:
            print('Send message error:', request.request, request.text)
            return False

        if not request.status_code == 200:
            # проверим статус пришедшего ответа
            return False


with open('.token', 'r') as t:
    TOKEN = re.sub('^\s+|\n|\r|\s+$', '', t.read())

with open('words', 'r') as f:
    words = f.readlines()

offset = 0

while True:
    try:
        check_updates()
        time.sleep(5)
    except KeyboardInterrupt:
        print('Interrupted by the user')
        break
