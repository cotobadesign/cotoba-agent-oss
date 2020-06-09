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
"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from programy.utils.logging.ylogger import YLogger
import yaml

from programy.storage.stores.file.store.filestore import FileStore

from programy.storage.entities.nlu import NLUStore


class FileNLUStore(FileStore, NLUStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def _load_file_contents(self, nlu_collection, filename):
        YLogger.debug(self, "Loading NLU_Servers [%s]", filename)
        server_index = 0
        try:
            with open(filename, 'r+', encoding="utf-8") as yml_file:
                yaml_data = yaml.load(yml_file)
                if yaml_data is not None:
                    nlu_section = self._get_section(yaml_data, 'nlu')
                    if nlu_section is not None:
                        if type(nlu_section) is not list:
                            nlu_section = [nlu_section]
                        for server_info in nlu_section:
                            url = self._get_yaml_option(server_info, "url")
                            if url is not None:
                                apikey = self._get_yaml_option(server_info, "apikey")
                                server_name = str(server_index)
                                nlu_collection.add_server(server_name, url, apikey, filename, server_index)
                            else:
                                error_info = "url parameter not found"
                                nlu_collection.set_error_info(filename, server_index, error_info)
                            server_index += 1
                    else:
                        error_info = "nlu section not found"
                        nlu_collection.set_error_info(filename, None, error_info)

        except Exception as excep:
            YLogger.exception(self, "Failed to load NLU_Servers [%s]", excep, filename)
            error_info = "illegal yaml format"
            nlu_collection.set_error_info(filename, 0, error_info)

    def _get_section(self, yaml_data, section_name):
        if section_name in yaml_data:
            return yaml_data[section_name]
        return None

    def _get_yaml_option(self, section, option_name):
        if option_name in section:
            return section[option_name]
        return None

    def _get_storage_path(self):
        return self._storage_engine.configuration.nlu_servers_storage.file

    def load(self, collection):
        servers_path = self._get_storage_path()
        collection.empty()
        self._load_file_contents(collection, servers_path)

    def reload_all(self, collection):
        servers_path = self._get_storage_path()
        collection.empty()
        self._load_file_contents(collection, servers_path)
