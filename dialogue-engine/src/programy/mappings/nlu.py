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
Copyright(c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files(the "Software"), to deal in the Software without restriction, including without limitation
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
from programy.storage.factory import StorageFactory
from programy.utils.language.japanese import JapaneseLanguage


class NluServerInfo(object):

    def __init__(self, url=None, apikey=None):
        self._url = url
        self._apikey = apikey

    @property
    def url(self):
        return self._url

    @property
    def apikey(self):
        return self._apikey


class NluCollection(object):

    def __init__(self, client, nlu_configration, errors_dict=None):
        self._set_matchlist = False
        if nlu_configration.use_file is not None:
            self._set_matchlist = nlu_configration.use_file

        if errors_dict is None:
            self._errors_dict = None
        else:
            errors_dict['nlu_servers'] = []
            self._errors_dict = errors_dict['nlu_servers']

        if nlu_configration.url is None or nlu_configration.url == '':
            self._defaultInfo = None
        else:
            self._defaultInfo = NluServerInfo(nlu_configration.url, nlu_configration.apikey)

        self._timeout = nlu_configration.timeout

        self._servers = []
        self._serverInfo = {}
        self._match_nlus = []
        self._check_urls = []

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, timeout):
        self._timeout = timeout

    @property
    def set_matchlist(self):
        return self._set_matchlist

    @property
    def servers(self):
        return self._servers

    @property
    def match_nlus(self):
        return self._match_nlus

    def empty(self):
        self._servers.clear()
        self._serverInfo.clear()
        self._match_nlus.clear()
        self._check_urls.clear()

    def remove(self, server_name):
        try:
            self._servers.remove(server_name)
        except Exception:
            pass
        self._serverInfo.pop(server_name, None)

    def set_servers_error(self, filename, index, description):
        if self._errors_dict is not None:
            error_info = {'file': filename, 'server-index': index, 'description': description}
            self._errors_dict.append(error_info)

    def set_nlus_error(self, filename, index, description):
        if self._errors_dict is not None:
            error_info = {'file': filename, 'nlu-index': index, 'description': description}
            self._errors_dict.append(error_info)

    def set_timeout_error(self, filename, value):
        if self._errors_dict is not None:
            description = "invalid timeout parameter[%s]" % value
            error_info = {'file': filename, 'description': description}
            self._errors_dict.append(error_info)

    def add_server(self, name, url, apikey, filename=None, index=0):
        server_name = self._convert_name(name)
        if server_name is None:
            YLogger.debug(self, "NLU parameter no server_name")
            return

        if server_name in self._servers:
            error_info = "NLU server [%s] already exist" % name
            self.set_servers_error(filename, index, error_info)
            return

        if url is None:
            error_info = "invalid url[%s] apikey[%s]" % (url, apikey)
            self.set_servers_error(filename, index, error_info)
            return
        else:
            url = url.strip()
            if url == '':
                error_info = "invalid url[%s] apikey[%s]" % (url, apikey)
                self.set_servers_error(filename, index, error_info)
                return

        if apikey is None:
            apikey = ''
        else:
            apikey = apikey.strip()
            if apikey == '' or apikey == 'None':
                apikey = ''

        YLogger.debug(self, "Adding NLU server name[%s] url[%s] apikey[%s] to server_list", server_name, url, apikey)
        server_info = NluServerInfo(url, apikey)
        self._servers.append(server_name)
        self._serverInfo[server_name] = server_info

    def add_nlu_by_url(self, url, apikey, filename=None, index=0):
        if url is None:
            error_info = "invalid url[%s] apikey[%s]" % (url, apikey)
            self.set_nlus_error(filename, index, error_info)
            return
        else:
            url = url.strip()
            if url == '':
                error_info = "invalid url[%s] apikey[%s]" % (url, apikey)
                self.set_nlus_error(filename, index, error_info)
                return

        if apikey is None:
            apikey = ''
        else:
            apikey = apikey.strip()
            if apikey == '' or apikey == 'None':
                apikey = ''

        if url in self._check_urls:
            error_info = "Duplicate url[%s] apikey[%s]" % (url, apikey)
            self.set_nlus_error(filename, index, error_info)
            return

        YLogger.debug(self, "Adding Matching-NLU url[%s] apikey[%s] to nlu_list", url, apikey)
        server_info = NluServerInfo(url, apikey)
        server_name = "NONAME-" + str(index)
        self._servers.append(server_name)
        self._match_nlus.append(server_name)
        self._serverInfo[server_name] = server_info
        self._check_urls.append(url)

    def add_nlu_by_name(self, name, filename=None, index=0):
        server_name = self._convert_name(name)
        if server_name is None:
            YLogger.debug(self, "NLU parameter no server_name")
            return

        server_info = self.server_info(server_name)
        if server_info is None:
            error_info = "NLU server name[%s] not found" % server_name
            self.set_nlus_error(filename, index, error_info)
            return

        if server_info.url in self._check_urls:
            error_info = "Duplicate url[%s] in name[%s]" % (server_info.url, server_name)
            self.set_nlus_error(filename, index, error_info)
            return

        YLogger.debug(self, "Adding Matching-NLU server_name[%s] to nlu_list", name)
        self._match_nlus.append(server_name)
        self._check_urls.append(server_info.url)

    def contains(self, name):
        server_name = self._convert_name(name)
        return bool(server_name in self._servers)

    def server_info(self, name):
        server_name = self._convert_name(name)
        if self.contains(server_name) is False:
            return None

        return self._serverInfo[server_name]

    def _convert_name(self, name):
        if name is None:
            return name
        else:
            name = name.strip()
            if name == '':
                return None

        server_name = JapaneseLanguage.zenhan_normalize(name)
        server_name = server_name.upper()
        return server_name

    def load(self, storage_factory):
        if storage_factory.entity_storage_engine_available(StorageFactory.NLU_SERVERS) is True:
            nlu_storage_engine = storage_factory.entity_storage_engine(StorageFactory.NLU_SERVERS)
            if nlu_storage_engine:
                nlu_storage_store = nlu_storage_engine.nlu_store()
                if nlu_storage_engine:
                    nlu_storage_store.load(self)

    def make_match_nlu_list(self):
        if len(self._match_nlus) == 0:
            if self._defaultInfo is not None:
                self._servers.append('DEFAULT')
                self._match_nlus.append('DEFAULT')
                self._serverInfo['DEFAULT'] = self._defaultInfo
            else:
                YLogger.debug(self, "NLU server not defined")
