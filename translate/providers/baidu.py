#!/usr/bin/env python
# encoding: utf-8

import json
import random
import requests
from hashlib import md5

from .base import BaseProvider
from ..exceptions import TranslationError


class BaiduProvider(BaseProvider):
    '''
    @BaiduProvider: This is a integration with Baidu Translator API.
    Website: https://fanyi.baidu.com/
    Documentation: https://fanyi-api.baidu.com/doc/21
    '''
    name = 'Baidu'
    base_url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    session = None

    def __init__(self, appid=None, **kwargs):
        try:
            super().__init__(**kwargs)
        except TypeError:
            super(BaiduProvider, self).__init__(**kwargs)

        self.appid = appid
        self.appkey = self.secret_access_key

    def _make_md5(self, s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    def _make_request(self, text):
        self.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})

        salt = random.randint(32768, 65536)
        sign = self._make_md5(self.appid + text + str(salt) + self.appkey)

        params = {'appid': self.appid, 'q': text, 'from': self.from_lang, 'to': self.to_lang, 'salt': salt,
                  'sign': sign}

        if self.session is None:
            self.session = requests.Session()
        response = self.session.post(self.base_url, params=params, headers=self.headers)
        response.raise_for_status()

        return json.loads(response.text)

    def get_translation(self, text):
        data = self._make_request(text)

        if "error_code" in data:
            raise TranslationError(data["error_msg"])

        return data['trans_result'][0]['dst']
