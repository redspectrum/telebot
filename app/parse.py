import requests
# from main import write_json
import re


def parse_text(text):
    pattern = r'/\w+'
    currency = re.search(pattern, text).group()
    return currency[1:]


def get_price(currency):
    url = 'https://belarusbank.by/api/kursExchange?city=Минск'
    r = requests.get(url).json()
    price = r[0]['{}_in'.format(currency.upper())]
    return price


def main():
    print(get_price(parse_text('сколько /eur ')))


if __name__ == '__main__':
    main()