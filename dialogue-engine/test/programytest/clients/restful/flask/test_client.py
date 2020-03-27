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
import unittest.mock
import os

from programy.clients.restful.flask.client import FlaskRestBotClient
from programy.clients.restful.client import UserInfo

from programytest.clients.arguments import MockArgumentParser


class MockFlaskRestBotClient(FlaskRestBotClient):

    def __init__(self, argument_parser=None):
        FlaskRestBotClient.__init__(self, "flask", argument_parser)
        self.aborted = False
        self.answer = None
        self.ask_question_exception = False

    def server_abort(self, status_code):
        self.aborted = True
        raise Exception("Pretending to abort!")

    def ask_question(self, userid, question, userInfo, deleteVariable, loglevel):
        if self.ask_question_exception is True:
            raise Exception("Something bad happened")
        return self.answer, question


class RestBotClientTests(unittest.TestCase):

    def test_rest_client_init(self):
        arguments = MockArgumentParser()
        client = FlaskRestBotClient("flask", arguments)
        self.assertIsNotNone(client)

    def test_verify_api_key_usage_inactive(self):
        arguments = MockArgumentParser()
        client = FlaskRestBotClient("flask", arguments)
        self.assertIsNotNone(client)
        client.configuration.client_configuration._use_api_keys = False
        request = unittest.mock.Mock()
        self.assertEqual((None, None), client.verify_api_key_usage(request))

    def test_get_api_key(self):
        arguments = MockArgumentParser()
        client = FlaskRestBotClient("flask", arguments)

        request = unittest.mock.Mock()
        request.args = {}
        request.args['apikey'] = '11111111'

        self.assertEqual('11111111', client.get_api_key(request))

    def test_verify_api_key_usage_active(self):
        arguments = MockArgumentParser()
        client = FlaskRestBotClient("flask", arguments)
        self.assertIsNotNone(client)
        client.configuration.client_configuration._use_api_keys = True
        client.configuration.client_configuration._api_key_file = os.path.dirname(__file__) + os.sep + ".." + os.sep + ".." + os.sep + "api_keys.txt"
        client.load_api_keys()
        request = unittest.mock.Mock()
        request.args = {}
        request.args['apikey'] = '11111111'
        self.assertEqual((None, None), client.verify_api_key_usage(request))

    def test_verify_api_key_usage_active_no_apikey(self):
        arguments = MockArgumentParser()
        client = MockFlaskRestBotClient(arguments)
        client.configuration.client_configuration._use_api_keys = True

        request = unittest.mock.Mock()
        request.args = {}

        response = client.verify_api_key_usage(request)
        self.assertIsNotNone(response)

    def test_verify_api_key_usage_active_invalid_apikey(self):
        arguments = MockArgumentParser()
        client = MockFlaskRestBotClient(arguments)
        client.configuration.client_configuration._use_api_keys = True

        request = unittest.mock.Mock()
        request.args = {}
        request.args['apikey'] = 'invalid'

        response = client.verify_api_key_usage(request)
        self.assertIsNotNone(response)

    def test_get_question(self):
        arguments = MockArgumentParser()
        client = FlaskRestBotClient("flask", arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890", "utterance": "Hello"}'

        self.assertEqual("Hello", client.get_question(request))

    def test_get_question_no_question(self):
        arguments = MockArgumentParser()
        client = MockFlaskRestBotClient(arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890", "utterance": null}'

        self.assertEqual("None", client.get_question(request))

    def test_get_question_none_question(self):
        arguments = MockArgumentParser()
        client = MockFlaskRestBotClient(arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890"}'

        self.assertEqual("None", client.get_question(request))

    def test_get_userid(self):
        arguments = MockArgumentParser()
        client = FlaskRestBotClient("flask", arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890"}'

        self.assertEqual("1234567890", client.get_userid(request))

    def test_get_userid_no_userid(self):
        arguments = MockArgumentParser()
        client = MockFlaskRestBotClient(arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{}'

        self.assertEqual("None", client.get_userid(request))

    def test_get_userid_none_userid(self):
        arguments = MockArgumentParser()
        client = MockFlaskRestBotClient(arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{"userId": null}'

        self.assertEqual("None", client.get_userid(request))

    def test_format_success_response(self):
        arguments = MockArgumentParser()
        client = FlaskRestBotClient("flask", arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890"}'
        userInfo = UserInfo(client, request)

        response = client.format_success_response("1234567890", "Hello", "Hi", userInfo)
        self.assertIsNotNone(response)
        self.assertEqual("1234567890", response['userId'])
        self.assertEqual("Hello", response['utterance'])
        self.assertEqual("Hi", response['response'])
        self.assertEqual("None", response['topic'])

    def test_format_error_response(self):
        arguments = MockArgumentParser()
        client = FlaskRestBotClient("flask", arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890"}'
        userInfo = UserInfo(client, request)

        response = client.format_error_response("1234567890", "Hello", "Something Bad", userInfo)
        self.assertIsNotNone(response)
        self.assertEqual("1234567890", response['userId'])
        self.assertEqual("Hello", response['utterance'])
        self.assertEqual("", response['response'])
        self.assertEqual("None", response['topic'])
        self.assertEqual("Something Bad", response['error'])

    def test_process_request(self):
        arguments = MockArgumentParser()
        client = MockFlaskRestBotClient(arguments)
        self.assertIsNotNone(client)
        client.configuration.client_configuration._use_api_keys = False

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890", "utterance": "Hello"}'

        client.answer = "Hi"

        response, _ = client.process_request(request)
        self.assertIsNotNone(response)
        self.assertEqual("1234567890", response['userId'])
        self.assertEqual("Hello", response['utterance'])
        self.assertEqual("Hi", response['response'])

    def test_process_request_no_api_key(self):
        arguments = MockArgumentParser()
        client = MockFlaskRestBotClient(arguments)
        self.assertIsNotNone(client)
        client.configuration.client_configuration._use_api_keys = True

        request = unittest.mock.Mock()
        request.args = {}
        request.data = b'{"userId": "1234567890", "utterance": "Hello"}'

        client.answer = "Hi"

        response, status = client.process_request(request)
        self.assertIsNotNone(response)
        self.assertEqual(status, 401)

    def test_process_request_exception(self):
        arguments = MockArgumentParser()
        client = MockFlaskRestBotClient(arguments)
        self.assertIsNotNone(client)
        client.configuration.client_configuration._use_api_keys = False

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890", "utterance": "Hello"}'

        client.answer = "Hi"
        client.ask_question_exception = True

        response, status = client.process_request(request)
        self.assertIsNotNone(response)
        self.assertEqual(status, 500)

    def test_ask_question(self):
        arguments = MockArgumentParser()
        client = FlaskRestBotClient("yadlan", arguments)
        self.assertIsNotNone(client)
        client.configuration.client_configuration._debug = True

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890", "utterance": "Hello"}'

        response, _ = client.process_request(request)
        self.assertIsNotNone(response)
        self.assertEqual("1234567890", response['userId'])
        self.assertEqual("Hello.", response['utterance'])
        self.assertEqual("", response['response'])
