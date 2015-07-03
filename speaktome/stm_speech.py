# -*- coding: utf-8 -*-


import yaml
import os
from urllib.request import Request


CONFIG_DIR = 'config'
APIKEY_FILENAME = 'keys.yml'
LANGUAGE_ES_ES = 'es_ES'
GOOGLE_SPEECH_URL = 'https://www.google.com/speech-api/v2/recognize?output=json&lang=%s&key=%s'


class Speech:
    def __init__(self, language=LANGUAGE_ES_ES):
        self.language = language
        self._api_key = None

    def _open_wav_file(self, path_file):
        pass

    def request(self):


class KeyApi:
    def __init__(self):
        self._path = os.path.dirname(os.path.abspath(__file__))
        self._config_path = os.path.join(self._path, CONFIG_DIR)
        self.config_file = os.path.join(self._config_path, APIKEY_FILENAME)
        self._data = None

    def _open(self):
        try:
            with open(self.config_file) as source:
                self._data = yaml.load(source)
                return True
        except:
            return False

    def get_api_key(self):
        if not self._open():
            return None

        if 'apikey' not in self._data:
            return None
