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
from programy.utils.logging.ylogger import YLogger

from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.botnames import BotNamesStore

import yaml


class FileBotNamesStore(FileStore, BotNamesStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def _get_storage_path(self):
        return self._storage_engine.configuration.bot_names_storage.file

    def _load_file_contents(self, collection, filename):
        YLogger.debug(self, "Loading bot_names from [%s]", filename)

        bot_index = 0
        try:
            with open(filename, 'r+', encoding="utf-8") as yml_file:
                yaml_data = yaml.load(yml_file, Loader=yaml.SafeLoader)
                if yaml_data is not None:
                    bot_section = self._get_section(yaml_data, 'bot')
                    if bot_section is not None:
                        bot_names = self._get_keys(bot_section)
                        for name in bot_names:
                            bot_yaml = self._get_section(bot_section, name)
                            bot_info, error_info = self._make_botname_info(collection, bot_yaml)
                            if error_info is None:
                                collection.add_botname(name, bot_info, filename, bot_index)
                            else:
                                collection.set_error_info(filename, bot_index, error_info)
                            bot_index += 1
                    else:
                        error_info = "bot section not found"
                        collection.set_error_info(filename, None, error_info)

        except Exception as excep:
            YLogger.exception(self, "Failed to load bot_names [%s]", excep, filename)
            error_info = "illegal yaml format"
            collection.set_error_info(filename, None, error_info)

    def _make_botname_info(self, collection, bot_yaml):
        error_info = None
        url = self._get_yaml_option(bot_yaml, 'url')
        apikey = self._get_yaml_option(bot_yaml, 'apikey')
        bot_info = collection.make_botInfo(url, apikey)
        if bot_info.url is None:
            error_info = "illegal basic parameter url=[%s] apikey=[%s]" % (url, apikey)
            return None, error_info

        locale = self._get_yaml_option(bot_yaml, 'locale')
        if bot_info.set_locale(locale) is False:
            error_info = "invalid locale parameter [%s]" % locale
            return None, error_info
        time = self._get_yaml_option(bot_yaml, 'time')
        if bot_info.set_time(time) is False:
            error_info = "invalid time parameter [%s]" % time
            return None, error_info
        topic = self._get_yaml_option(bot_yaml, 'topic')
        if bot_info.set_topic(topic) is False:
            error_info = "invalid topic parameter [%s]" % topic
            return None, error_info
        deleteVariable = self._get_yaml_bool_option(bot_yaml, 'deleteVariable')
        if bot_info.set_deleteVariable(deleteVariable) is False:
            error_info = "invalid deleteVariable parameter [%s]" % deleteVariable
            return None, error_info
        config = self._get_yaml_option(bot_yaml, 'config')
        if bot_info.set_config(config) is False:
            error_info = "invalid config parameter [%s]" % config
            return None, error_info
        metadata = self._get_yaml_option(bot_yaml, 'metadata')
        if bot_info.set_metadata(metadata) is False:
            error_info = "invalid metadata parameter [%s]" % metadata
            return None, error_info

        return bot_info, error_info

    def _get_section(self, yaml_data, section_name):
        if section_name in yaml_data:
            return yaml_data[section_name]
        return None

    def _get_keys(self, section):
        return section.keys()

    def _get_yaml_option(self, section, option_name):
        if option_name in section:
            return section[option_name]
        return None

    def _get_yaml_bool_option(self, section, option_name):
        if option_name in section:
            option_value = section[option_name]
            if isinstance(option_value, bool):
                return option_value
            else:
                try:
                    value = bool(option_value)
                    return value
                except Exception:
                    return option_value
        return None

    def get_storage(self):
        return self.storage_engine.configuration.bot_names_storage

    def load(self, collection):
        botnames_path = self._get_storage_path()
        self._load_file_contents(collection, botnames_path)

    def reload_all(self, collection):
        botnames_path = self._get_storage_path()
        self._load_file_contents(collection, botnames_path)
