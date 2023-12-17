#!/usr/bin/env python
# encoding: utf-8

from .mymemory_translated import MyMemoryProvider  # noqa
from .microsoft import MicrosoftProvider  # noqa
from .deepl import DeeplProvider  # noqa
from .libre import LibreProvider
from .google import GoogleProvider
from .baidu import BaiduProvider
from .qcri import QcriProvider
from .niutrans import NiutransProvider

__all__ = ['MyMemoryProvider', 'MicrosoftProvider', 'DeeplProvider',
           'LibreProvider', 'GoogleProvider', 'BaiduProvider',
           'QcriProvider', 'NiutransProvider']
