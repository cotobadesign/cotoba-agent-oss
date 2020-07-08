"""
Copyright (c) 2020 COTOBA DESIGN, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import re
import json
import iso8601

from programy.utils.logging.ylogger import YLogger

from programy.storage.factory import StorageFactory
from programy.utils.language.japanese import JapaneseLanguage


class PublicBotInfo(object):

    def __init__(self, url=None, apikey=None):
        self._url = url
        self._apikey = apikey
        self._header = {'Content-Type': 'application/json;charset=UTF-8'}

        if apikey is None:
            self._header['x-api-key'] = ''
        else:
            apikey = apikey.strip()
            self._header['x-api-key'] = apikey

        self._locale = None
        self._time = None
        self._topic = None
        self._metadata = None
        self._deleteVariable = False
        self._config = None

    @property
    def url(self):
        return self._url

    @property
    def header(self):
        return self._header

    @property
    def apikey(self):
        return self._apikey

    @property
    def locale(self):
        return self._locale

    @property
    def time(self):
        return self._time

    @property
    def topic(self):
        return self._topic

    @property
    def metadata(self):
        return self._metadata

    @property
    def deleteVariable(self):
        return self._deleteVariable

    @property
    def config(self):
        return self._config

    def set_locale(self, locale):
        self._locale = None
        if locale is None:
            return True
        locale = locale.strip()
        if locale == '':
            return True

        if '-' not in locale:
            YLogger.debug(self, "botInfo <locale> invalid format: [%s]" % locale)
            return False
        else:
            locale_param = locale.split('-')
            if len(locale_param) != 2:
                YLogger.debug(self, "botInfo <locale> invalid format: [%s]" % locale)
                return False
            else:
                if len(locale_param[0]) != 2 and len(locale_param[0]) != 3:
                    YLogger.debug(self, "botInfo <locale> invalid lunguage_code: [%s]" % locale)
                    return False
                if len(locale_param[1]) != 2 and len(locale_param[1]) != 3:
                    YLogger.debug(self, "botInfo <locale> invalid country_code: [%s]" % locale)
                    return False
                if locale_param[0].islower() is False:
                    YLogger.debug(self, "botInfo <locale> lunguage_code is not lower: [%s]" % locale)
                    return False
                if locale_param[1].isupper() is False:
                    YLogger.debug(self, "botInfo <locale> country_code is not upper: [%s]" % locale)
                    return False

        self._locale = locale
        return True

    def set_time(self, time):
        self._time = None
        if time is None:
            return True
        time = time.strip()
        if time == '':
            return True

        try:
            iso8601.parse_date(time)
        except Exception:
            YLogger.debug(self, "botInfo <time> datetime parser error: [%s]" % time)
            return False

        self._time = time
        return True

    def set_topic(self, topic):
        self._topic = None
        if topic is None:
            return True
        topic = topic.strip()
        if topic == '' or topic == '*':
            return True

        self._topic = topic
        return True

    def set_metadata(self, metadata):
        self._metadata = None
        if metadata is None or metadata == '':
            return True

        try:
            self._metadata = json.loads(metadata)
        except Exception:
            self._metadata = metadata

        return True

    def set_deleteVariable(self, deleteVariable):
        self._deleteVariable = False
        if deleteVariable is None:
            return True

        if type(deleteVariable) is str:
            deleteVariable = deleteVariable.strip()
            if deleteVariable == '':
                return True
            value = deleteVariable.upper()
            if value == "FALSE":
                deleteVariable = False
            elif value == "TRUE":
                deleteVariable = True
            else:
                YLogger.debug(self, "botInfo <deleteVariable> not boolean: [%s]" % deleteVariable)
                return False
        elif type(deleteVariable) is not bool:
            YLogger.debug(self, "botInfo <deleteVariable> not boolean: [%s]" % deleteVariable)
            return False

        self._deleteVariable = deleteVariable
        return True

    def set_config(self, config):
        self._config = None
        if config is None:
            return True
        config = config.strip()
        if config == '':
            return True

        try:
            self._config = json.loads(config)
        except Exception:
            YLogger.debug(self, "botInfo <config> not JSON format: [%s]" % config)
            return False

        return True

    def join_metadata(self, metadata):
        if self._metadata is None:
            self.set_metadata(metadata)
            return

        if metadata is None:
            return
        if metadata == '':
            self._metadata = None
            return

        try:
            join_metadata = json.loads(metadata)
        except Exception:
            join_metadata = metadata

        if type(self._metadata) is dict and type(join_metadata) is dict:
            for key, value in join_metadata.items():
                if value is None:
                    if key in self._metadata.keys():
                        del self._metadata[key]
                        continue
                self._metadata[key] = value
        else:
            self._metadata = join_metadata


class BotNamesCollection(object):

    def __init__(self, errors_dict=None):
        self._botnames = {}

        if errors_dict is None:
            self._errors_dict = None
        else:
            errors_dict['bot_names'] = []
            self._errors_dict = errors_dict['bot_names']

    @property
    def botnames(self):
        return self._botnames

    def empty(self):
        self._botnames.clear()

    def botInfo(self, name):
        bot_name = JapaneseLanguage.zenhan_normalize(name)
        bot_name = bot_name.upper()
        if bot_name in self._botnames:
            return self._botnames[bot_name]
        return None

    def set_error_info(self, filename, index, description):
        if self._errors_dict is not None:
            error_info = {'file': filename, 'index': index, 'description': description}
            self._errors_dict.append(error_info)

    def make_botInfo(self, url, apikey):
        if url is None:
            return None
        url = url.strip()
        if url == '':
            return None
        botInfo = PublicBotInfo(url, apikey)
        return botInfo

    def add_botname(self, name, botInfo, filename, line):
        bot_name = JapaneseLanguage.zenhan_normalize(name)
        bot_name = bot_name.upper()
        if bot_name not in self._botnames:
            self._botnames[bot_name] = botInfo
        else:
            error_info = "duplicate botname='%s' (url='%s' is invalid)" % (name, botInfo.url)
            self.set_error_info(filename, line, error_info)
            return

    def remove(self, name):
        bot_name = JapaneseLanguage.zenhan_normalize(name)
        bot_name = bot_name.upper()
        if bot_name in self._botnames:
            del self._botnames[bot_name]

    def contains(self, name):
        bot_name = JapaneseLanguage.zenhan_normalize(name)
        bot_name = bot_name.upper()
        return bool(bot_name in self._botnames)

    def load(self, storage_factory):
        if storage_factory.entity_storage_engine_available(StorageFactory.BOT_NAMES) is True:
            botnames_store_engine = storage_factory.entity_storage_engine(StorageFactory.BOT_NAMES)
            if botnames_store_engine:
                try:
                    botnames_store = botnames_store_engine.bot_names_store()
                    botnames_store.load_all(self)
                except Exception as e:
                    YLogger.exception(self, "Failed to load BotNames from storage", e)

        return len(self._botnames)

    def reload(self, storage_factory):
        if storage_factory.entity_storage_engine_available(StorageFactory.BOT_NAMES) is True:
            botnames_engine = storage_factory.entity_storage_engine(StorageFactory.BOT_NAMES)
            if botnames_engine:
                try:
                    botnames_store = botnames_engine.botids_store()
                    botnames_store.reload(self)
                except Exception as e:
                    YLogger.exception(self, "Failed to load BotNames from storage", e)
