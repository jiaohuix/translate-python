#!/usr/bin/env python
# encoding: utf-8

import requests
import json

from .base import BaseProvider
from ..exceptions import TranslationError


class QcriProvider(BaseProvider):
    '''
    @QcriProvider: This is a integration with Qcri Translator API.
    Website: https://mt.qcri.org/api/
    Documentation: https://mt.qcri.org/api/v1/ref
    '''
    name = 'Qcri'
    base_url = 'https://mt.qcri.org/api/v1/translate'
    session = None

    def __init__(self, domain="general", **kwargs):
        try:
            super().__init__(**kwargs)
        except TypeError:
            super(QcriProvider, self).__init__(**kwargs)

        self.languages = '{}-{}'.format(self.from_lang, self.to_lang)
        self.domain = domain

    def _make_request(self, text):

        params = {
            'key': self.secret_access_key,
            'langpair': self.languages,
            'domain': self.domain,
            'text': text
        }

        if self.session is None:
            self.session = requests.Session()
        response = self.session.get(self.base_url, params=params, headers=self.headers)
        response.raise_for_status()

        return json.loads(response.text)

    def get_translation(self, text):
        data = self._make_request(text)

        if "error" in data:
            raise TranslationError(data["error"])

        return data["translatedText"]
