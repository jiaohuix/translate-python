#!/usr/bin/env python
# encoding: utf-8

import re
import html
import requests

from .base import BaseProvider
from ..exceptions import TranslationError


class GoogleProvider(BaseProvider):
    '''
    @GoogleProvider: This is a integration with Google Translator API.
    Website: https://translate.google.com/
    Documentation: https://cloud.google.com/translate/docs?hl=zh-cn
    '''
    name = 'Google'
    base_url = 'http://translate.google.com/m'
    session = None

    def _make_request(self, text):
        params = {
            'q': text,
            'tl': self.to_lang,
            'sl': self.from_lang,
        }

        if self.session is None:
            self.session = requests.Session()
        response = self.session.get(self.base_url, params=params, headers=self.headers)
        response.raise_for_status()

        expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
        result = re.findall(expr, response.text)
        success = bool(len(result) != 0)
        data = {"success": success}
        if success:
            data["translation"] = html.unescape(result[0])
        else:
            data["error"] = "No translation result found."
        return data

    def get_translation(self, text):
        data = self._make_request(text)

        if "error" in data:
            raise TranslationError(data["error"])

        return data["translation"]
