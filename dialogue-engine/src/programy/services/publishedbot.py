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
import json

from programy.services.service import Service
from programy.config.brain.service import BrainServiceConfiguration


class PublishedBotAPI(object):

    def __init__(self, request_api=None):
        if request_api is None:
            self._requests_api = requests
        else:
            self._requests_api = request_api

    def post(self, url, header, data):
        return self._requests_api.post(url, headers=header, data=data)


class PublishedBotService(Service):

    def __init__(self, config: BrainServiceConfiguration, api=None):
        Service.__init__(self, config)

        if api is None:
            self.api = PublishedBotAPI()
        else:
            self.api = api

        self._botInfo = None
        self._userId = None
        self._status_code = ''

    @property
    def botInfo(self):
        return self._botInfo

    @property
    def userId(self):
        return self._userId

    @botInfo.setter
    def botInfo(self, botInfo):
        self._botInfo = botInfo

    @userId.setter
    def userId(self, userId):
        self._userId = userId

    def _format_payload(self, client_context, botInfo, question):
        payload = {}

        payload.update({'userId': self._userId})
        payload.update({'utterance': question})

        if botInfo.locale is not None:
            payload.update({'locale': botInfo.locale})
        if botInfo.time is not None:
            payload.update({'time': botInfo.time})
        if botInfo.topic is not None:
            payload.update({'topic': botInfo.topic})
        if botInfo.deleteVariable is not None:
            payload.update({'deleteVariable': botInfo.deleteVariable})
        if botInfo.metadata is not None:
            payload.update({'metadata': botInfo.metadata})
        if botInfo.config is not None:
            payload.update({'config': botInfo.config})

        json_payload = json.dumps(payload)

        return json_payload

    def get_status_code(self):
        return self._status_code

    def ask_question(self, client_context, question: str):
        self._status_code = ''

        if self._botInfo is None or self._userId is None:
            YLogger.debug(client_context, "No botName Info or userId ")
            return ""

        if question is None or question == '':
            YLogger.debug(client_context, "Question is empty")
            return ""

        bot_url = self._botInfo.url

        try:
            headers = self._botInfo.header
            payload = self._format_payload(client_context, self._botInfo, question)
            bodys = payload.encode('UTF-8')

            self._status_code = '000'
            response = self.api.post(bot_url, header=headers, data=bodys)
            self._status_code = str(response.status_code)
            if response.status_code == 200:
                return response.text
            else:
                YLogger.debug(client_context, "Error status code[%d]", response.status_code)
                return ""

        except Exception as excep:
            YLogger.error(client_context, "Failed to Public-Bot Comminucation: %s", str(excep))

        return ""
