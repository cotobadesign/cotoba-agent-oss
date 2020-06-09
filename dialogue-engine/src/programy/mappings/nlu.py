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
        if errors_dict is None:
            self._errors_dict = None
        else:
            errors_dict['nlu_servers'] = []
            self._errors_dict = errors_dict['nlu_servers']

        if nlu_configration.url is None or nlu_configration.url == '':
            self._defaultInfo = None
        else:
            self._defaultInfo = NluServerInfo(nlu_configration.url, nlu_configration.apikey)

        self._servers = []
        self._serverInfo = {}
        self._check_urls = []

        if nlu_configration.use_file is True:
            self.make_nlu_list(client)

        if len(self._servers) == 0:
            if self._defaultInfo is not None:
                self._servers.append('default')
                self._serverInfo['default'] = self._defaultInfo

        if len(self._servers) == 0:
            YLogger.debug(self, "NLU server not defined")

    @property
    def servers(self):
        return self._servers

    def empty(self):
        self._servers.clear()
        self._serverInfo.clear()
        self._check_urls.clear()

    def remove(self, server_name):
        try:
            self._servers.remove(server_name)
        except Exception:
            pass
        self._serverInfo.pop(server_name, None)

    def set_error_info(self, filename, index, description):
        if self._errors_dict is not None:
            error_info = {'file': filename, 'index': index, 'description': description}
            self._errors_dict.append(error_info)

    def add_server(self, server_name, url, apikey, filename=None, index=0):
        if server_name is None:
            YLogger.debug(self, "NLU parameter no server_name")
            return

        server_name = server_name.strip()
        if server_name in self._servers:
            YLogger.debug(self, "NLU server [%s] already exist", server_name)
            return

        if url is None or url == '':
            if self._defaultInfo is None:
                error_info = "invalid url[%s] apikey[%s]" % (url, apikey)
                self.set_error_info(filename, index, error_info)
                return
            else:
                url = self._defaultInfo.url
        else:
            url = url.strip()
        if apikey is None or apikey == '' or apikey == 'None':
            apikey = ''
        else:
            try:
                apikey = apikey.strip()
            except Exception:
                apikey = ''

        if url in self._check_urls:
            error_info = "Duplicate url[%s] apikey[%s]" % (url, apikey)
            self.set_error_info(filename, index, error_info)
            return

        YLogger.debug(self, "Adding NLU server_name[%s] url[%s] apikey[%s] to server_list", server_name, url, apikey)
        server = NluServerInfo(url, apikey)
        self._servers.append(server_name)
        self._serverInfo[server_name] = server
        self._check_urls.append(url)

    def contains(self, server_name):
        return bool(server_name in self._servers)

    def server_info(self, server_name):
        if self.contains(server_name) is False:
            return None

        return self._serverInfo[server_name]

    def make_nlu_list(self, client):
        storage_factory = client.storage_factory
        if storage_factory.entity_storage_engine_available(StorageFactory.NLU_SERVERS) is True:
            nlu_storage_engine = storage_factory.entity_storage_engine(StorageFactory.NLU_SERVERS)
            if nlu_storage_engine:
                nlu_storage_store = nlu_storage_engine.nlu_store()
                if nlu_storage_engine:
                    nlu_storage_store.load(self)
