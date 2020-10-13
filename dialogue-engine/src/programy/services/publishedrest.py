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
import time
from requests.exceptions import Timeout

from programy.services.service import Service
from programy.config.brain.service import BrainServiceConfiguration


class PublishedRestAPI(object):

    def __init__(self, request_api=None):
        if request_api is None:
            self._requests_api = requests
        else:
            self._requests_api = request_api

    def get(self, url, query, header, body, timeout=None):
        return self._requests_api.get(url, params=query, headers=header, data=body, timeout=timeout)

    def post(self, url, query, header, body, timeout=None):
        return self._requests_api.post(url, params=query, headers=header, data=body, timeout=timeout)

    def put(self, url, query, header, body, timeout=None):
        return self._requests_api.put(url, params=query, headers=header, data=body, timeout=timeout)

    def delete(self, url, query, header, body, timeout=None):
        return self._requests_api.delete(url, params=query, headers=header, data=body, timeout=timeout)

    def patch(self, url, query, header, body, timeout=None):
        return self._requests_api.patch(url, params=query, headers=header, data=body, timeout=timeout)


class PublishedRestService(Service):

    def __init__(self, config: BrainServiceConfiguration, api=None):
        Service.__init__(self, config)

        if api is None:
            self.api = PublishedRestAPI()
        else:
            self.api = api

        self._params = None
        self._status_code = ''
        self._latency = ''

        self._start_time = None
        self._end_time = None

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params):
        self._params = params

    def check_char_type(self):
        char_type = None
        is_XML = False
        header = self.params.header

        if header is None or type(header) is not dict:
            return char_type, is_XML

        content_type = None
        for header_key in header:
            if header_key.upper() == 'CONTENT-TYPE':
                content_type = header[header_key]
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

    def get_latency(self):
        return self._latency

    def _check_latency(self):
        self._end_time = time.time()
        latency = self._end_time - self._start_time
        return str(latency)

    def ask_question(self, client_context, question: str, timeout=10):
        self._status_code = ''
        self._latency = ''

        if self.params is None:
            return ""

        if self.params.host is None:
            return ""

        if len(self.params.query) > 0:
            query_list = self.params.query
            for key, value in query_list.items():
                if key == "":
                    YLogger.debug(client_context, "Query key is empty: {"": %s}", value)
                    return ""
            try:
                query = urllib.parse.urlencode(query_list)
            except Exception as excep:
                YLogger.debug(client_context, "Failed to encode query: %s", str(excep))
                return ""
        else:
            query = None

        if len(self.params.header) > 0:
            header = self.params.header
        else:
            header = None

        if self.params.body is not None:
            body_data = self.params.body
            char_type, is_XML = self.check_char_type()
            if is_XML is True:
                try:
                    xml_dict = json.loads(body_data)
                    body_data = xmltodict.unparse(xml_dict)
                except Exception as excep:
                    YLogger.debug(client_context, "Failed to convert JSON to XML: %s", str(excep))
                    return ""

            if char_type is not None:
                body = body_data.encode(char_type)
            else:
                body = body_data
        else:
            body = None

        self._start_time = time.time()
        try:
            self._status_code = '000'
            if self.params.method == 'GET':
                response = self.api.get(self.params.host, query=query, header=header, body=body, timeout=timeout)
            elif self.params.method == 'POST':
                response = self.api.post(self.params.host, query=query, header=header, body=body, timeout=timeout)
            elif self.params.method == 'PUT':
                response = self.api.put(self.params.host, query=query, header=header, body=body, timeout=timeout)
            elif self.params.method == 'DELETE':
                response = self.api.delete(self.params.host, query=query, header=header, body=body, timeout=timeout)
            elif self.params.method == 'PATCH':
                response = self.api.patch(self.params.host, query=query, header=header, body=body, timeout=timeout)
            else:
                raise Exception("Unsupported REST method [%s]" % self.params.method)

            self._latency = self._check_latency()
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

        except Timeout as excep:
            self._status_code = '001'
            self._latency = self._check_latency()
            YLogger.debug(client_context, "General-REST Comminucation Timeout: %s", str(excep))
        except Exception as excep:
            self._latency = self._check_latency()
            YLogger.debug(client_context, "Failed to General-REST Comminucation: %s", str(excep))

        return ""
