#!/usr/bin/env python
# encoding: utf-8

import requests
import json

from .base import BaseProvider
from ..constants import TRANSLATION_FROM_DEFAULT
from ..exceptions import TranslationError


class NiutransProvider(BaseProvider):
    '''
    @NiutransProvider: This is a integration with Niutrans Translator API.
    Website: https://niutrans.com/trans?type=text
    Documentation: https://niutrans.com/documents/contents/trans_text

    dictNo(String)  Set the sub-library ID of the terminology dictionary, default value is empty
    memoryNo(String)  Set the sub-library ID of the translation memory, default value is empty
    '''
    name = 'Niutrans'
    base_url = 'https://api.niutrans.com/NiuTransServer/translation'
    session = None

    def __init__(self, dictNo=None, memoryNo=None, **kwargs):
        try:
            super().__init__(**kwargs)
        except TypeError:
            super(NiutransProvider, self).__init__(**kwargs)

        self.apikey = self.secret_access_key
        self.dictNo = dictNo
        self.memoryNo = memoryNo

    def _make_request(self, text):

        params = {
            'apikey': self.apikey,
            'from': self.from_lang,
            'to': self.to_lang,
            'src_text': text
        }

        if not self.dictNo is None:
            params["dictNo"] = self.dictNo

        if not self.memoryNo is None:
            params["memoryNo"] = self.memoryNo

        if self.session is None:
            self.session = requests.Session()
        response = self.session.post(self.base_url, params=params)
        response.raise_for_status()
        return json.loads(response.text)

    def get_translation(self, text):
        data = self._make_request(text)
        if "error_code" in data:
            raise TranslationError(data["error_msg"])

        return data["tgt_text"]
