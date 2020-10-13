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
        nlu_index = 0
        try:
            with open(filename, 'r+', encoding="utf-8") as yml_file:
                yaml_data = yaml.load(yml_file, Loader=yaml.SafeLoader)
                if yaml_data is not None:
                    servers_section = self._get_section(yaml_data, 'servers')
                    if servers_section is not None:
                        servers = self._get_keys(servers_section)
                        for server in servers:
                            server_info = self._get_section(servers_section, server)
                            url = self._get_yaml_option(server_info, "url")
                            if url is not None:
                                apikey = self._get_yaml_option(server_info, "apikey")
                                nlu_collection.add_server(server, url, apikey, filename, server_index)
                            else:
                                error_info = "url parameter not found in servers"
                                nlu_collection.set_servers_error(filename, server_index, error_info)
                            server_index += 1

                    if nlu_collection.set_matchlist is True:
                        nlu_section = self._get_section(yaml_data, 'nlu')
                        if nlu_section is not None:
                            if type(nlu_section) is not list:
                                nlu_section = [nlu_section]
                            for server_info in nlu_section:
                                name = self._get_yaml_option(server_info, "name")
                                if name is not None:
                                    if nlu_collection.server_info(name) is None:
                                        error_info = "server[%s] not found" % name
                                        nlu_collection.set_nlus_error(filename, nlu_index, error_info)
                                        nlu_index += 1
                                        continue
                                url = self._get_yaml_option(server_info, "url")
                                if url is not None:
                                    if name is not None:
                                        error_info = "exist both parameters name[%s] and url[%s]" % (name, url)
                                        nlu_collection.set_nlus_error(filename, nlu_index, error_info)
                                    else:
                                        apikey = self._get_yaml_option(server_info, "apikey")
                                        nlu_collection.add_nlu_by_url(url, apikey, filename, nlu_index)
                                else:
                                    if name is not None:
                                        nlu_collection.add_nlu_by_name(name, filename, nlu_index)
                                    else:
                                        error_info = "url parameter not found in nlu"
                                        nlu_collection.set_nlus_error(filename, nlu_index, error_info)
                                nlu_index += 1
                        else:
                            error_info = "nlu section not found"
                            nlu_collection.set_nlus_error(filename, 0, error_info)

                        timeout_val = self._get_section(yaml_data, 'timeout')
                        if timeout_val is not None:
                            timeout = 0
                            if type(timeout_val) is int:
                                timeout = timeout_val
                            elif type(timeout_val) is str:
                                try:
                                    timeout = int(timeout)
                                except Exception:
                                    pass
                            if timeout > 0:
                                nlu_collection.timeout = timeout
                            else:
                                nlu_collection.set_timeout_error(filename, timeout_val)

        except Exception as excep:
            YLogger.exception(self, "Failed to load NLU_Servers [%s]", excep, filename)
            error_info = "illegal yaml format"
            nlu_collection.set_servers_error(filename, 0, error_info)

    def _get_section(self, yaml_data, section_name):
        if section_name in yaml_data:
            return yaml_data[section_name]
        return None

    def _get_keys(self, section):
        return section.keys()

    def _get_yaml_option(self, section, option_name):
        if type(section) is not dict:
            return None
        if option_name in section:
            if section[option_name] is None:
                return None
            elif type(section[option_name]) is str:
                return section[option_name]
            else:
                return str(section[option_name])
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
