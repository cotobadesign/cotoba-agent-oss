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

    DEFAULT_PUBLIC_BOT_HOST = "cotobadesign.com"
    DEFAULT_PUBLIC_BOT_PATH = "/published-bots/%s/ask"

    def __init__(self, config: BrainServiceConfiguration, api=None):
        Service.__init__(self, config)

        if api is None:
            self.api = PublishedBotAPI()
        else:
            self.api = api

        if config.host is None:
            self.host = self.DEFAULT_PUBLIC_BOT_HOST
        else:
            self.host = config.host

        self._org_botId = None
        self._org_apiKey = None

        self._botId = None
        self._botHost = None
        self._locale = None
        self._time = None
        self._userId = None
        self._topic = None
        self._deleteVariable = None
        self._metadata = None
        self._config = None
        self._status_code = ''

    @property
    def botId(self):
        return self._botId

    @property
    def botHost(self):
        return self._botHost

    @property
    def locale(self):
        return self._locale

    @property
    def time(self):
        return self._time

    @property
    def userId(self):
        return self._userId

    @property
    def topic(self):
        return self._topic

    @property
    def deleteVariable(self):
        return self._deleteVariable

    @property
    def metadata(self):
        return self._metadata

    @property
    def config(self):
        return self._config

    @botId.setter
    def botId(self, botId):
        self._botId = botId

    @botHost.setter
    def botHost(self, botHost):
        self._botHost = botHost

    @locale.setter
    def locale(self, locale):
        self._locale = locale

    @time.setter
    def time(self, time):
        self._time = time

    @userId.setter
    def userId(self, userId):
        self._userId = userId

    @topic.setter
    def topic(self, topic):
        self._topic = topic

    @deleteVariable.setter
    def deleteVariable(self, deleteVariable):
        self._deleteVariable = deleteVariable

    @metadata.setter
    def metadata(self, metadata):
        self._metadata = metadata

    @config.setter
    def config(self, config):
        self._config = config

    def _make_userId(self, client_context):
        userId = self._org_botId
        if hasattr(client_context, 'userInfo') is True:
            userId = userId + '_' + client_context.userInfo.get('__USER_USERID__')
        return userId

    def _format_payload(self, client_context, question):
        payload = {}

        if self._locale is not None:
            if self._locale != '':
                payload.update({'locale': self._locale})
        elif hasattr(client_context, 'userInfo') is True:
            user_locale = client_context.userInfo.get('__USER_LOCALE__')
            if user_locale != 'None':
                payload.update({'locale': user_locale})
        if self._time is not None:
            if self._time != '':
                payload.update({'time': self._time})
        elif hasattr(client_context, 'userInfo') is True:
            user_time = client_context.userInfo.get('__USER_TIME__')
            if user_time != 'None':
                payload.update({'time': user_time})

        if self._userId is not None:
            if self._userId == '':
                payload.update({'userId': self._make_userId(client_context)})
            else:
                payload.update({'userId': self._userId})
        else:
            payload.update({'userId': self._make_userId(client_context)})

        if self._topic is not None:
            if self._topic != '':
                payload.update({'topic': self._topic})
        else:
            payload.update({'topic': '*'})
        payload.update({'utterance': question})
        if self._deleteVariable is not None:
            payload.update({'deleteVariable': self._deleteVariable})

        metadata = None
        if self._metadata is not None:
            if self._metadata != '':
                try:
                    metadata = json.loads(self._metadata)
                except Exception:
                    metadata = self._metadata
        elif hasattr(client_context, 'userInfo') is True:
            user_metadata = client_context.userInfo.get('__USER_METADATA__')
            if user_metadata != 'None':
                try:
                    metadata = json.loads(user_metadata)
                except Exception:
                    metadata = user_metadata
        if metadata is not None:
            payload.update({'metadata': metadata})

        if self._config is not None:
            if self._config != '':
                try:
                    configdata = json.loads(self._config)
                    payload.update({'config': configdata})
                except Exception:
                    pass

        json_payload = json.dumps(payload)

        return json_payload

    def get_status_code(self):
        return self._status_code

    def ask_question(self, client_context, question: str):
        self._status_code = ''

        self._org_botId = client_context.bot.brain.configuration.bot_name
        self._org_apiKey = client_context.bot.brain.configuration.manager_name

        if self._botId is None or self._org_apiKey is None:
            YLogger.debug(client_context, "No botID or API-Key")
            return ""

        if question is None or question == '':
            YLogger.debug(client_context, "Question is empty")
            return ""

        if self._botHost is None:
            host = self.host
        else:
            host = self._botHost
        bot_url = host + self.DEFAULT_PUBLIC_BOT_PATH % self._botId

        try:
            headers = {'Content-Type': 'application/json:charset=UTF-8', 'x-api-key': self._org_apiKey}
            payload = self._format_payload(client_context, question)
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
