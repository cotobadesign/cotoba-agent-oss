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

from programy.services.publishedbot import PublishedBotService, PublishedBotAPI
from programy.services.service import BrainServiceConfiguration
from programy.mappings.botnames import PublicBotInfo

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

    def post(self, url, headers, data, timeout=None):
        return MockRequestsResponse(self._response, 200)


class MockPublishedBotAPI(object):

    def __init__(self, status=200, response=None, throw_exception=False):
        self._status_code = status
        self._response = response
        self._throw_exception = throw_exception

    def post(self, url, header, data, timeout=None):
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

        bot_info = PublicBotInfo("https://cotobadesign.co.jp/bots/PublishedBot/ask", 'api_key')

        bot_info._locale = "ja-JP"
        bot_info._time = "2019-01-01T00:00:00+09:00"
        bot_info._topic = "morning"
        bot_info._deleteVariable = True
        bot_info._metadata = "Test Data"
        bot_info._config = '{"logLevel": "debug"}'

        service.botInfo = bot_info
        service.userId = "user00"

        self.assertEqual(service.botInfo.url, "https://cotobadesign.co.jp/bots/PublishedBot/ask")
        self.assertEqual(service.botInfo.apikey, 'api_key')
        self.assertEqual(service.botInfo.locale, "ja-JP")
        self.assertEqual(service.botInfo.time, "2019-01-01T00:00:00+09:00")
        self.assertEqual(service.botInfo.topic, "morning")
        self.assertEqual(service.botInfo.deleteVariable, True)
        self.assertEqual(service.botInfo.metadata, "Test Data")
        self.assertEqual(service.botInfo.config, '{"logLevel": "debug"}')

        self.assertEqual(service.userId, "user00")
        self.assertEqual(service.botInfo.header['Content-Type'], "application/json;charset=UTF-8")
        self.assertEqual(service.botInfo.header['x-api-key'], "api_key")

    def test_ask_question(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        bot_info = PublicBotInfo("https://cotobadesign.co.jp/bots/PublishedBot/ask", 'api_key')

        bot_info._locale = None
        bot_info._time = None
        bot_info._topic = None
        bot_info._deleteVariable = None
        bot_info._metadata = None
        bot_info._config = None

        service.botInfo = bot_info
        service.userId = "user00"

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('{"response": "Hello"}', response)
        self.assertEqual('200', service._status_code)

    def test_ask_question_all_parameter(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        bot_info = PublicBotInfo("https://cotobadesign.co.jp/bots/PublishedBot/ask", 'api_key')

        bot_info._locale = "ja-JP"
        bot_info._time = "2019-01-01T00:00:00+09:00"
        bot_info._topic = "morning"
        bot_info._deleteVariable = True
        bot_info._metadata = "Test Data"
        bot_info._config = '{"logLevel": "debug"}'

        service.botInfo = bot_info
        service.userId = "user00"

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('{"response": "Hello"}', response)
        self.assertEqual('200', service._status_code)

    def test_ask_question_no_parameter(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        bot_info = PublicBotInfo("https://cotobadesign.co.jp/bots/PublishedBot/ask", 'api_key')

        service.botInfo = bot_info
        service.userId = "user00"

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('{"response": "Hello"}', response)
        self.assertEqual('200', service._status_code)

    def test_ask_question_no_botInfo(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        service.userId = "user00"

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('', response)
        self.assertEqual('', service._status_code)

    def test_ask_question_no_userid(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        bot_info = PublicBotInfo("https://cotobadesign.co.jp/bots/PublishedBot/ask", 'api_key')

        bot_info._locale = "ja-JP"
        bot_info._time = "2019-01-01T00:00:00+09:00"
        bot_info._topic = "morning"
        bot_info._deleteVariable = True
        bot_info._metadata = "Test Data"
        bot_info._config = '{"logLevel": "debug"}'

        service.botInfo = bot_info

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('', response)
        self.assertEqual('', service._status_code)

    def test_ask_question_no_question(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        bot_info = PublicBotInfo("https://cotobadesign.co.jp/bots/PublishedBot/ask", 'api_key')

        bot_info._locale = "ja-JP"
        bot_info._time = "2019-01-01T00:00:00+09:00"
        bot_info._topic = "morning"
        bot_info._deleteVariable = True
        bot_info._metadata = "Test Data"
        bot_info._config = '{"logLevel": "debug"}'

        service.botInfo = bot_info
        service.userId = "user00"

        response = service.ask_question(self._client_context, None)
        self.assertEqual('', response)
        self.assertEqual('', service._status_code)

    def test_ask_question_empty_question(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        bot_info = PublicBotInfo("https://cotobadesign.co.jp/bots/PublishedBot/ask", 'api_key')

        bot_info._locale = "ja-JP"
        bot_info._time = "2019-01-01T00:00:00+09:00"
        bot_info._topic = "morning"
        bot_info._deleteVariable = True
        bot_info._metadata = "Test Data"
        bot_info._config = '{"logLevel": "debug"}'

        service.botInfo = bot_info
        service.userId = "user00"

        response = service.ask_question(self._client_context, "")
        self.assertEqual('', response)
        self.assertEqual('', service._status_code)

    def test_ask_question_none_setting(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('', response)
        self.assertEqual('', service._status_code)

    def test_ask_question_no_apikey(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        bot_info = PublicBotInfo("https://cotobadesign.co.jp/bots/PublishedBot/ask", None)

        bot_info._locale = "ja-JP"
        bot_info._time = "2019-01-01T00:00:00+09:00"
        bot_info._topic = "morning"
        bot_info._deleteVariable = True
        bot_info._metadata = "Test Data"
        bot_info._config = '{"logLevel": "debug"}'

        service.botInfo = bot_info

        self.assertEqual(service.botInfo.header['x-api-key'], "")
        service.userId = "user00"

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('{"response": "Hello"}', response)
        self.assertEqual('200', service._status_code)

    def test_ask_question_empty_apikey(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        bot_info = PublicBotInfo("https://cotobadesign.co.jp/bots/PublishedBot/ask", '')

        bot_info._locale = "ja-JP"
        bot_info._time = "2019-01-01T00:00:00+09:00"
        bot_info._topic = "morning"
        bot_info._deleteVariable = True
        bot_info._metadata = "Test Data"
        bot_info._config = '{"logLevel": "debug"}'

        service.botInfo = bot_info
        service.userId = "user00"

        self.assertEqual(service.botInfo.header['x-api-key'], "")

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('{"response": "Hello"}', response)
        self.assertEqual('200', service._status_code)

    def test_ask_question_Illegal_status(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(status=500, response=response_data)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        bot_info = PublicBotInfo("https://cotobadesign.co.jp/bots/PublishedBot/ask", 'api_key')

        bot_info._locale = "ja-JP"
        bot_info._time = "2019-01-01T00:00:00+09:00"
        bot_info._topic = "morning"
        bot_info._deleteVariable = True
        bot_info._metadata = "Test Data"
        bot_info._config = '{"logLevel": "debug"}'

        service.botInfo = bot_info
        service.userId = "user00"

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('', response)
        self.assertEqual('500', service._status_code)

    def test_ask_question_exception(self):

        config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        config._host = "test_publishdbot"

        response_data = '{"response": "Hello"}'
        request_api = MockPublishedBotAPI(response=response_data, throw_exception=True)
        service = PublishedBotService(config=config, api=request_api)
        self.assertIsNotNone(service)

        bot_info = PublicBotInfo("https://cotobadesign.co.jp/bots/PublishedBot/ask", 'api_key')

        bot_info._locale = "ja-JP"
        bot_info._time = "2019-01-01T00:00:00+09:00"
        bot_info._topic = "morning"
        bot_info._deleteVariable = True
        bot_info._metadata = "Test Data"
        bot_info._config = '{"logLevel": "debug"}'

        service.botInfo = bot_info
        service.userId = "user00"

        question = "Hello"
        response = service.ask_question(self._client_context, question)
        self.assertEqual('', response)
        self.assertEqual('000', service._status_code)
