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
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

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
import requests
import urllib
import json
import xmltodict

from programy.services.service import Service
from programy.config.brain.service import BrainServiceConfiguration


class PublishedRestAPI(object):

    def __init__(self, request_api=None):
        if request_api is None:
            self._requests_api = requests
        else:
            self._requests_api = request_api

    def get(self, url, query, header, body):
        return self._requests_api.get(url, params=query, headers=header, data=body)

    def post(self, url, query, header, body):
        return self._requests_api.post(url, params=query, headers=header, data=body)

    def put(self, url, query, header, body):
        return self._requests_api.put(url, params=query, headers=header, data=body)

    def delete(self, url, query, header, body):
        return self._requests_api.delete(url, params=query, headers=header, data=body)

    def patch(self, url, query, header, body):
        return self._requests_api.patch(url, params=query, headers=header, data=body)


class PublishedRestService(Service):

    def __init__(self, config: BrainServiceConfiguration, api=None):
        Service.__init__(self, config)

        if api is None:
            self.api = PublishedRestAPI()
        else:
            self.api = api

        self._host = None
        self._method = None
        self._query = None
        self._header = None
        self._body = None
        self._status_code = ''

    @property
    def host(self):
        return self._host

    @property
    def method(self):
        return self._method

    @property
    def query(self):
        return self._query

    @property
    def header(self):
        return self._header

    @property
    def body(self):
        return self._body

    @host.setter
    def host(self, host):
        self._host = host

    @method.setter
    def method(self, method):
        self._method = method

    @query.setter
    def query(self, query):
        self._query = query

    @header.setter
    def header(self, header):
        self._header = header

    @body.setter
    def body(self, body):
        self._body = body

    def check_char_type(self):
        char_type = None
        is_XML = False
        if self._header is None or type(self._header) is not dict:
            return char_type, is_XML

        content_type = None
        for header_key in self._header:
            if header_key.upper() == 'CONTENT-TYPE':
                content_type = self._header[header_key]
                break
        if content_type is not None:
            params = content_type.split(';')
            for param in params:
                value = param.split('=')
                if len(value) == 1:
                    if value[0] == "application/xml" or value[0] == "text/xml":
                        is_XML = True
                if len(value) == 2:
                    if value[0].strip().upper() == "CHARSET":
                        char_type = value[1].replace("'", "").strip()

        return char_type, is_XML

    def get_status_code(self):
        return self._status_code

    def ask_question(self, client_context, question: str):
        self._status_code = ''

        if self._host is None:
            return ""

        if self._query is not None:
            for key, value in self._query.items():
                if key == "":
                    YLogger.debug(client_context, "Query key is empty: {"": %s}", value)
                    return ""
            try:
                query = urllib.parse.urlencode(self._query)
            except Exception as excep:
                YLogger.debug(client_context, "Failed to encode query: %s", str(excep))
                return ""
        else:
            query = None

        if self.body is not None:
            char_type, is_XML = self.check_char_type()
            if is_XML is True:
                try:
                    xml_dict = json.loads(self.body)
                    self.body = xmltodict.unparse(xml_dict)
                except Exception as excep:
                    YLogger.debug(client_context, "Failed to convert JSON to XML: %s", str(excep))
                    return ""

            if char_type is not None:
                body = self.body.encode(char_type)
            else:
                body = self.body
        else:
            body = None

        try:
            self._status_code = '000'
            if self._method == 'GET':
                response = self.api.get(self._host, query=query, header=self._header, body=body)
            elif self.method == 'POST':
                response = self.api.post(self._host, query=query, header=self._header, body=body)
            elif self.method == 'PUT':
                response = self.api.put(self._host, query=query, header=self._header, body=body)
            elif self.method == 'DELETE':
                response = self.api.delete(self._host, query=query, header=self._header, body=body)
            elif self.method == 'PATCH':
                response = self.api.patch(self._host, query=query, header=self._header, body=body)
            else:
                raise Exception("Unsupported REST method [%s]" % self._method)

            self._status_code = str(response.status_code)
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type')
                if content_type is not None:
                    params = content_type.split(';')
                    for param in params:
                        if param == 'text/xml' or param == 'application/xml':
                            try:
                                xml_dict = xmltodict.parse(response.text)
                                json_text = json.dumps(xml_dict, ensure_ascii=False)
                                return json_text
                            except Exception as excep:
                                YLogger.debug(client_context, "Failed to convert Response-XML to JSON-text: %s", str(excep))
                                return ""
                return response.text
            else:
                YLogger.debug(client_context, "Error status code[%d]", response.status_code)
                return ""

        except Exception as excep:
            YLogger.debug(client_context, "Failed to General-REST Comminucation: %s", str(excep))

        return ""
