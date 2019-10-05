from flask import Flask
from flask_sslify import SSLify
from flask import request
from flask import jsonify
import requests
import json
import re
import time

app = Flask(__name__)
sslify = SSLify(app)

TOKEN = ''
URL = 'https://api.telegram.org/bot{}/'.format(TOKEN)

def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def send_message(chat_id, text='default text'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()

def parse_text(text):
    pattern = r'/\w+'
    currency = re.search(pattern, text)
    return currency.group()[1:] if currency else None

def get_price(currency):
    url = 'https://belarusbank.by/api/kursExchange?city=Минск'
    r = requests.get(url).json()
    price = r[0]['{}_in'.format(currency.upper())]
    return price

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']

        command = parse_text(message)
        if command:
            if 'start' in command or 'info' in command:
                text = 'Hello! My name Dolobori Bot!\n\n' \
                       'My commands:\n' \
                       '/info - get info about me\n' \
                       '/login - check login\n' \
                       '/balance - check balance\n' \
                       '/bonus - check bonus\n' \
                       '/friends - check friends'
                send_message(chat_id, text=text)
            elif 'login' in command:
                send_message(chat_id, text='Проверяю!')
                time.sleep(3)
                send_message(chat_id, text='Вы не зарегистрированы! Пройдите регистрацию по ссылке:')
            elif 'password' in command:
                send_message(chat_id, text='Проверяю!')
            elif 'balance' in command:
                send_message(chat_id, text='Проверяю!')
                time.sleep(3)
                send_message(chat_id, text='Ваш баланс: 10000 рублей')
            elif 'bonus' in command:
                send_message(chat_id, text='Поздравляем! Вы получили бонус!')
            elif 'friends' in command:
                send_message(chat_id, text='Проверяю!')
                time.sleep(3)
                send_message(chat_id, text='У Вас много друзей!')
            # elif 'usd' in message:
            #     price = get_price(parse_text(message))
            #     send_message(chat_id, text=price)
        if 'как дела' in message.lower():
            send_message(chat_id, text='Какие могут быть дела у бездушной машины))')
        elif 'привет' in message.lower():
            send_message(chat_id, text='И Вам Привет!')
        elif 'погода' in message.lower():
            send_message(chat_id, text='Отличная погода!')

        # Write into file (may be for login/pass)
        # write_json(r)

        # # Return back message
        # return jsonify(r)

    return '<h1>Bot welcomes You!</h1>'

if __name__ == '__main__':
    app.run()