from datetime import datetime, timezone, timedelta
import json
from time import time

import requests

urls = {
    'latestblock': 'https://blockchain.info/latestblock',
    'difficulty': 'https://blockchain.info/q/getdifficulty',
    'blockcount': 'https://blockchain.info/q/getblockcount',
    'latesthash': 'https://blockchain.info/q/latesthash',
    'bcperblock': 'https://blockchain.info/q/bcperblock',
    'totalbc': 'https://blockchain.info/q/totalbc',
    'probability': 'https://blockchain.info/q/probability',
    'hashestowin': 'https://blockchain.info/q/hashestowin',
    'nextretarget': 'https://blockchain.info/q/nextretarget',
    'avgtxsize': 'https://blockchain.info/q/avgtxsize',
    'avgtxvalue': 'https://blockchain.info/q/avgtxvalue',
    'interval': 'https://blockchain.info/q/interval',
    'eta': 'https://blockchain.info/q/eta',
    'avgtxnumber': 'https://blockchain.info/q/avgtxnumber'
    }


def initialize():
    now_data = fetch(urls['latestblock'])
    now_difficulty = fetch(urls['difficulty'])
    data = {
        'time': now_data['time'],
        'height': now_data['height'],
        'difficulty': now_difficulty
        }
    write(data)


def fetch(url):
    res = requests.get(url)
    res = res.json()
    return res


def write(data):
    with open("BlockTimer.json", mode="wt", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def read():
    with open("BlockTimer.json", mode="r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def main():
    now_data = fetch(urls['latestblock'])
    now_difficulty = fetch(urls['difficulty'])
    past_data = read()
    if not now_data['height'] == past_data['height']:
        def_time = round((now_data['time'] - past_data['time']) / 60)
        now_time = datetime.fromtimestamp(time(), timezone(timedelta(hours=+9), 'JST')).strftime(
            '%Y-%m-%d %H:%M'
            )
        if def_time > 60:
            evaluation = '⏳' * 3
        elif 60 >= def_time >= 45:
            evaluation = '⏳' * 2
        elif 45 > def_time >= 30:
            evaluation = '⏳' * 1
        else:
            evaluation = ''

        msg = f'{now_time} ■{now_data["height"]}  生成時間: {def_time}分 {evaluation}'
        print(msg)

    past_difficulty = past_data['difficulty']
    if not past_difficulty == now_difficulty:
        msg = f'@everyone 難易度変更: {past_difficulty} -> {now_difficulty}'
        print(msg)

    data = {
        'time': now_data['time'],
        'height': now_data['height'],
        'difficulty': now_difficulty
        }
    write(data)


if __name__ == '__main__':
    # initialize()
    main()
