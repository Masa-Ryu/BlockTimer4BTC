from datetime import datetime, timezone, timedelta
import json
from time import time

import requests


class BlockTimer:
    def __int__(self):
        self.urls = {
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

    def initialize(self):
        now_data = self.fetch(self.urls['latestblock'])
        now_difficulty = self.fetch(self.urls['difficulty'])
        data = {
            'time': now_data['time'],
            'height': now_data['height'],
            'difficulty': now_difficulty
            }
        self.write(data)

    def fetch(self, url):
        res = requests.get(url)
        res = res.json()
        return res

    def write(self, data):
        with open("BlockTimer.json", mode="wt", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def read(self):
        with open("BlockTimer.json", mode="r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def run(self):
        now_data = self.fetch(self.urls['latestblock'])
        now_difficulty = self.fetch(self.urls['difficulty'])
        past_data = self.read()
        caution = None
        if not now_data['height'] == past_data['height']:
            def_time = round((now_data['time'] - past_data['time']) / 60)
            now_time = datetime.fromtimestamp(
                time(), timezone(
                    timedelta(hours=+9), 'JST'
                    )
                ).strftime(
                '%Y-%m-%d %H:%M'
                )
            if def_time > 60:
                evaluation = '⏳' * 3
                caution = '@everyone CAUTION!'
            elif 60 >= def_time >= 45:
                evaluation = '⏳' * 2
            elif 45 > def_time >= 30:
                evaluation = '⏳' * 1
            else:
                evaluation = ''

            msg = f'{now_time} 生成時間: {def_time}分 {evaluation}'
        else:
            msg = None

        past_difficulty = past_data['difficulty']
        if not past_difficulty == now_difficulty:
            if past_difficulty < now_difficulty:
                result = 'UP'
            else:
                result = 'DOWN'
            difficulty = f'@everyone 難易度変更({result}): {past_difficulty} -> {now_difficulty}'
        else:
            difficulty = None

        data = {
            'time': now_data['time'],
            'height': now_data['height'],
            'difficulty': now_difficulty
            }
        self.write(data)
        return msg, caution, difficulty
