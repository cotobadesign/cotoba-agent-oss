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
import unittest
import json

from programy.services.publishedbot import PublishedBotService, PublishedBotAPI
from programy.services.service import BrainServiceConfiguration
from programy.clients.restful.client import UserInfo

from programytest.client import TestClient


class MockRequestsResponse(object):

    def __init__(self, data, status_code):
        self._data = data
        self._status_code = status_code

    @property
    def text(self):
        return self._data

    @property
    def status_code(self):
        return self._status_code


class MockPublishedBotRequest(object):

    def __init__(self, response=None):
        self._response = response

    def post(self, url, headers, data):
        return MockRequestsResponse(self._response, 200)


class MockPublishedBotAPI(object):

    def __init__(self, status=200, response=None, throw_exception=False):
        self._status_code = status
        self._response = response
        self._throw_exception = throw_exception

    def post(self, url, header, data):
        if self._throw_exception is True:
            raise Exception(self._response)
        else:
            return MockRequestsResponse(self._response, self._status_code)


class PublishedBotAPITests(unittest.TestCase):

    def test_api_post(self):

        response_data = 'Hello'
        moc_request = MockPublishedBotRequest(response=response_data)
        request_api = PublishedBotAPI(request_api=moc_request)
        url = ""
        headers = ""
        data = ""
        response = request_api.post(url, headers, data)
        self.assertIsNotNone(response)
        self.assertEqual(200, response.status_code)
        self.assertEqual('Hello', response.text)


class PublishedBotServiceTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = client.create_client_context("testid")

    def test_ask_question_set_parameter(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        service = PublishedBotService(config=config)
        self.assertIsNotNone(service)

        service._botId = "PublishedBot"
        service._botHost = "cotobadesign.co.jp"
        service._locale = "ja-JP"
        service._time = "2019-01-01T00:00:00+09:00"
        service._userId = "user00"
        service._topic = "morning"
        service._deleteVariable = True
        service._metadata = "Test Data"
        service._config = '{"logLevel": "debug"}'

        self.assertEqual(service.botId, "PublishedBot")
        self.assertEqual(service.botHost, "cotobadesign.co.jp")
        self.assertEqual(service.locale, "ja-JP")
        self.assertEqual(service.time, "2019-01-01T00:00:00+09:00")
        self.assertEqual(service.userId, "user00")
        self.assertEqual(service.topic, "morning")
        self.assertEqual(service.deleteVariable, True)
        self.assertEqual(service.metadata, "Test Data")
        self.assertEqual(service.config, '{"logLevel": "debug"}')

    def test_ask_question(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        self._client_context.bot.brain.configuration._bot_name = "RequestBot"
        self._client_context.bot.brain.configuration._manager_name = "Bot_API_key"

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        service.botId = "PublishedBot"
        service.botHost = None
        service.locale = None
        service.time = None
        service.userId = "user00"
        service.topic = None
        service.deleteVariable = None
        service.metadata = None
        service.config = None

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('{"response": "Hello"}', response)

    def test_ask_question_all_parameter(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        self._client_context.bot.brain.configuration._bot_name = "RequestBot"
        self._client_context.bot.brain.configuration._manager_name = "Bot_API_key"

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        service.botId = "PublishedBot"
        service.botHost = "cotobadesign.co.jp"
        service.locale = "ja-JP"
        service.time = "2019-01-01T00:00:00+09:00"
        service.userId = "user00"
        service.topic = "morning"
        service.deleteVariable = True
        service.metadata = "Test Data"
        service.config = '{"logLevel": "debug"}'

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('{"response": "Hello"}', response)

    def test_ask_question_with_userinfo(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        self._client_context.bot.brain.configuration._bot_name = "RequestBot"
        self._client_context.bot.brain.configuration._manager_name = "Bot_API_key"

        userInfo = UserInfo(None, None)
        userInfo.set("__USER_LOCALE__", "ja-JP")
        userInfo.set("__USER_TIME__", "2019-01-01T00:00:00+09:00")
        userInfo.set("__USER_METADATA__", "Test Data")
        self._client_context.userInfo = userInfo

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        service.botId = "PublishedBot"
        service.botHost = None
        service.locale = None
        service.time = None
        service.userId = "user00"
        service.topic = None
        service.deleteVariable = None
        service.metadata = None
        service.config = None

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('{"response": "Hello"}', response)

    def test_ask_question_default_host(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")

        self._client_context.bot.brain.configuration._bot_name = "RequestBot"
        self._client_context.bot.brain.configuration._manager_name = "Bot_API_key"

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        service.botId = "PublishedBot"
        service.botHost = None
        service.locale = None
        service.time = None
        service.userId = None
        service.topic = None
        service.deleteVariable = None
        service.metadata = None
        service.config = None

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('{"response": "Hello"}', response)

    def test_ask_question_default_userid(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        self._client_context.bot.brain.configuration._bot_name = "RequestBot"
        self._client_context.bot.brain.configuration._manager_name = "Bot_API_key"

        userInfo = UserInfo(None, None)
        userInfo.set("__USER_USERID__", "default_uesrid")
        userInfo.set("__USER_LOCALE__", "ja-JP")
        userInfo.set("__USER_TIME__", "2019-01-01T00:00:00+09:00")
        userInfo.set("__USER_METADATA__", None)
        self._client_context.userInfo = userInfo

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        service.botId = "PublishedBot"
        service.botHost = None
        service.locale = None
        service.time = None
        service.userId = None
        service.topic = None
        service.deleteVariable = None
        service.metadata = None
        service.config = None

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('{"response": "Hello"}', response)

    def test_ask_question_no_userid(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        self._client_context.bot.brain.configuration._bot_name = "RequestBot"
        self._client_context.bot.brain.configuration._manager_name = "Bot_API_key"

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        service.botId = "PublishedBot"
        service.botHost = None
        service.locale = None
        service.time = None
        service.userId = None
        service.topic = None
        service.deleteVariable = None
        service.metadata = None
        service.config = None

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('{"response": "Hello"}', response)

    def test_ask_question_no_userdata(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        self._client_context.bot.brain.configuration._bot_name = "RequestBot"
        self._client_context.bot.brain.configuration._manager_name = "Bot_API_key"

        userInfo = UserInfo(None, None)
        userInfo.set("__USER_LOCALE__", "None")
        userInfo.set("__USER_TIME__", "None")
        userInfo.set("__USER_METADATA__", "None")
        self._client_context.userInfo = userInfo

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        service.botId = "PublishedBot"
        service.botHost = None
        service.locale = None
        service.time = None
        service.userId = "user00"
        service.topic = None
        service.deleteVariable = None
        service.metadata = None
        service.config = None

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('{"response": "Hello"}', response)

    def test_ask_question_Illegal_status(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        self._client_context.bot.brain.configuration._bot_name = "RequestBot"
        self._client_context.bot.brain.configuration._manager_name = "Bot_API_key"

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(status=500, response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        service.botId = "PublishedBot"
        service.botHost = None
        service.locale = None
        service.time = None
        service.userId = "user00"
        service.topic = None
        service.deleteVariable = None
        service.metadata = None
        service.config = None

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('', response)

    def test_ask_question_no_parameter(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        self._client_context.bot.brain.configuration._bot_name = "RequestBot"
        self._client_context.bot.brain.configuration._manager_name = "Bot_API_key"

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('', response)

    def test_ask_question_no_botname(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        self._client_context.bot.brain.configuration._manager_name = "Bot_API_key"

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        service.botId = "PublishedBot"
        service.botHost = None
        service.locale = None
        service.time = None
        service.userId = "user00"
        service.topic = None
        service.deleteVariable = None
        service.metadata = None
        service.config = None

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('{"response": "Hello"}', response)

    def test_ask_question_no_apikey(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        self._client_context.bot.brain.configuration._bot_name = "RequestBot"

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        service.botId = "PublishedBot"
        service.botHost = None
        service.locale = None
        service.time = None
        service.userId = "user00"
        service.topic = None
        service.deleteVariable = None
        service.metadata = None
        service.config = None

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('', response)

    def test_ask_question_no_botid(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        self._client_context.bot.brain.configuration._bot_name = "RequestBot"
        self._client_context.bot.brain.configuration._manager_name = "Bot_API_key"

        userInfo = UserInfo(None, None)
        userInfo.set("__USER_LOCALE__", "ja-JP")
        userInfo.set("__USER_TIME__", "2019-01-01T00:00:00+09:00")
        userInfo.set("__USER_METADATA__", "Test Data")
        self._client_context.userInfo = userInfo

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        service.botId = None
        service.botHost = None
        service.locale = None
        service.time = None
        service.userId = "user00"
        service.topic = None
        service.deleteVariable = None
        service.metadata = None
        service.config = None

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('', response)

    def test_ask_question_exception(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        self._client_context.bot.brain.configuration._bot_name = "RequestBot"
        self._client_context.bot.brain.configuration._manager_name = "Bot_API_key"

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data, throw_exception=True)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        service.botId = "PublishedBot"
        service.botHost = None
        service.locale = None
        service.time = None
        service.userId = "user00"
        service.topic = None
        service.deleteVariable = None
        service.metadata = None
        service.config = None

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('', response)
