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
import requests
import json

from programy.utils.logging.ylogger import YLogger

from programy.nlu.nlu import NluRequest


class CotobadesignNlu(NluRequest):

    def __init__(self, config):
        NluRequest.__init__(self, config)

        self._requests_api = requests
        self._status_code = ''

    def set_request_api(self, api):
        self._requests_api = api

    def get_status_code(self):
        return self._status_code

    def nluCall(self, client_context, url, apikey, utterance):
        self._status_code = ''

        if utterance is None or utterance == '':
            return None

        if self._configuration.max_utterance_length > 0:
            if self._configuration.max_utterance_length < len(utterance):
                return None

        params = {
            "utterance": utterance,
        }
        json_data = json.dumps(params)

        headers = {'Content-Type': 'application/json', 'x-api-key': apikey}
        try:
            self._status_code = '000'
            response = self._requests_api.post(url=url, headers=headers, data=json_data)
            self._status_code = str(response.status_code)
            if response.status_code == 200:
                return response.text.strip()
            else:
                YLogger.debug(client_context, "NLU Error status code[%d]", response.status_code)
        except Exception as excep:
            YLogger.debug(client_context, "Failed to NLU Comminucation: %s", str(excep))

        return None
