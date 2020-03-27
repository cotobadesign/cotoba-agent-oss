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
import shutil

from programy.clients.restful.yadlan.flask.client import FlaskYadlanClient
from programy.clients.restful.client import UserInfo

from programytest.clients.arguments import MockArgumentParser


class MockFlaskYadlanClient(FlaskYadlanClient):

    def __init__(self, argument_parser=None):
        FlaskYadlanClient.__init__(self, "yadlan", argument_parser)
        self.aborted = False
        self.answer = None
        self.ask_question_exception = False

    def server_abort(self, error_code, error_msg):
        self.aborted = True
        raise Exception("Pretending to abort!")

    def ask_question(self, userid, question, userInfo, deleteVariable, loglevel):
        if self.ask_question_exception is True:
            raise Exception("Something bad happened")
        return self.answer, question


class FlaskYadlanClientTests(unittest.TestCase):

    def test_rest_client_init(self):
        arguments = MockArgumentParser()
        client = FlaskYadlanClient("yadlan", arguments)
        self.assertIsNotNone(client)

    def test_verify_api_key_usage_inactive(self):
        arguments = MockArgumentParser()
        client = FlaskYadlanClient("yadlan", arguments)
        self.assertIsNotNone(client)
        client.configuration.client_configuration._use_api_keys = False
        request = unittest.mock.Mock()
        self.assertEqual((None, None), client.verify_api_key_usage(request))

    def test_get_api_key(self):
        arguments = MockArgumentParser()
        client = FlaskYadlanClient("yadlan", arguments)

        request = unittest.mock.Mock()
        request.args = {}
        request.args['apikey'] = '11111111'

        self.assertEqual('11111111', client.get_api_key(request))

    def test_verify_api_key_usage_active(self):
        arguments = MockArgumentParser()
        client = FlaskYadlanClient("yadlan", arguments)
        self.assertIsNotNone(client)
        client.configuration.client_configuration._use_api_keys = True
        client.configuration.client_configuration._api_key_file = os.path.dirname(__file__) + os.sep + ".." + os.sep + ".." + os.sep + "api_keys.txt"
        client.load_api_keys()
        request = unittest.mock.Mock()
        request.args = {}
        request.args['apikey'] = '11111111'
        self.assertEqual(({'error': 'Unauthorized access'}, 401), client.verify_api_key_usage(request))

    def test_verify_api_key_usage_active_no_apikey(self):
        arguments = MockArgumentParser()
        client = MockFlaskYadlanClient(arguments)
        client.configuration.client_configuration._use_api_keys = True

        request = unittest.mock.Mock()
        request.args = {}

        response = client.verify_api_key_usage(request)
        self.assertIsNotNone(response)

    def test_verify_api_key_usage_active_invalid_apikey(self):
        arguments = MockArgumentParser()
        client = MockFlaskYadlanClient(arguments)
        client.configuration.client_configuration._use_api_keys = True

        request = unittest.mock.Mock()
        request.args = {}
        request.args['apikey'] = 'invalid'

        response = client.verify_api_key_usage(request)
        self.assertIsNotNone(response)

    def test_get_question(self):
        arguments = MockArgumentParser()
        client = FlaskYadlanClient("yadlan", arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890", "utterance": "Hello"}'

        self.assertEqual("Hello", client.get_question(request))

    def test_get_question_no_question(self):
        arguments = MockArgumentParser()
        client = MockFlaskYadlanClient(arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890", "utterance": null}'

        self.assertEqual("None", client.get_question(request))

    def test_get_question_none_question(self):
        arguments = MockArgumentParser()
        client = MockFlaskYadlanClient(arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890"}'

        self.assertEqual("None", client.get_question(request))

    def test_get_userid(self):
        arguments = MockArgumentParser()
        client = FlaskYadlanClient("yadlan", arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890"}'

        self.assertEqual("1234567890", client.get_userid(request))

    def test_get_userid_no_userid(self):
        arguments = MockArgumentParser()
        client = MockFlaskYadlanClient(arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{}'

        self.assertEqual("None", client.get_userid(request))

    def test_get_userid_none_userid(self):
        arguments = MockArgumentParser()
        client = MockFlaskYadlanClient(arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()

        request.data = b'{"userId": null}'
        self.assertEqual("None", client.get_userid(request))

        request.data = b'{"userId": ""}'
        self.assertEqual("None", client.get_userid(request))

    def test_get_other_data(self):
        arguments = MockArgumentParser()
        client = MockFlaskYadlanClient(arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()

        request.data = b'{"config": {"logLevel": "debug"}}'
        self.assertEqual("debug", client.get_config_option(request, 'logLevel'))
        self.assertEqual("debug", client.get_config_loglevel(request))

        request.data = b'{"config": {"logLevel": "DEBUG"}}'
        with self.assertRaises(Exception):
            client.get_config_loglevel(request)

        request.data = b'{"variables": {"test": "value"}}'
        self.assertEqual('{"test": "value"}', client.get_variables(request))

    def test_invalid_request_empty(self):
        arguments = MockArgumentParser()
        client = MockFlaskYadlanClient(arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b''

        with self.assertRaises(Exception):
            client.get_userid(request)
        self.assertTrue(client.aborted)

        with self.assertRaises(Exception):
            client.get_deleteVariable(request)
        self.assertTrue(client.aborted)

        with self.assertRaises(Exception):
            client.get_metadata(request)
        self.assertTrue(client.aborted)

        with self.assertRaises(Exception):
            client.get_config_option(request, 'logLevel')
        self.assertTrue(client.aborted)

        with self.assertRaises(Exception):
            client.get_variables(request)
        self.assertTrue(client.aborted)

    def test_invalid_request_not_json(self):
        arguments = MockArgumentParser()
        client = MockFlaskYadlanClient(arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'test_data, aaa'

        with self.assertRaises(Exception):
            client.get_userid(request)
        self.assertTrue(client.aborted)

        with self.assertRaises(Exception):
            client.get_deleteVariable(request)
        self.assertTrue(client.aborted)

        with self.assertRaises(Exception):
            client.get_metadata(request)
        self.assertTrue(client.aborted)

        with self.assertRaises(Exception):
            client.get_config_option(request, 'logLevel')
        self.assertTrue(client.aborted)

        with self.assertRaises(Exception):
            client.get_variables(request)
        self.assertTrue(client.aborted)

    def test_format_success_response(self):
        arguments = MockArgumentParser()
        client = FlaskYadlanClient("yadlan", arguments)
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
        client = FlaskYadlanClient("yadlan", arguments)
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
        client = MockFlaskYadlanClient(arguments)
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
        client = MockFlaskYadlanClient(arguments)
        self.assertIsNotNone(client)
        client.configuration.client_configuration._use_api_keys = True

        request = unittest.mock.Mock()
        request.args = {}
        request.data = b'{"userId": "1234567890", "utterance": "Hello"}'

        client.answer = "Hi"

        response, status = client.process_request(request)
        self.assertIsNotNone(response)
        self.assertEqual(status, 401)

    def test_process_request_no_question(self):
        arguments = MockArgumentParser()
        client = FlaskYadlanClient("yadlan", arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.args = {}
        request.data = b'{"userId": "1234567890"}'

        response, status = client.process_request(request)
        self.assertIsNotNone(response)
        self.assertEqual(status, 400)

    def test_process_request_exception(self):
        arguments = MockArgumentParser()
        client = MockFlaskYadlanClient(arguments)
        self.assertIsNotNone(client)
        client.configuration.client_configuration._use_api_keys = False

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890", "utterance": "Hello"}'

        client.answer = "Hi"
        client.ask_question_exception = True

        response, status = client.process_request(request)
        self.assertIsNotNone(response)
        self.assertEqual(status, 500)

    def test_checkBotVersion(self):
        arguments = MockArgumentParser()
        client = MockFlaskYadlanClient(arguments)
        self.assertIsNotNone(client)

        self.assertEqual(False, client.checkBotVersion('v1.0'))

        bot = client._bot_factory.select_bot()
        bot.configuration._version = 'v1.0'

        self.assertEqual(True, client.checkBotVersion('v1.0'))
        self.assertEqual(False, client.checkBotVersion('v1 0'))

    def test_dump_request(self):
        arguments = MockArgumentParser()
        client = FlaskYadlanClient("yadlan", arguments)
        self.assertIsNotNone(client)
        client.configuration.client_configuration._debug = True

        request = unittest.mock.Mock()
        response_data = "hello"

        latency = 1.0

        request.data = b'{"userId": "1234567890", "utterance": "Hello"}'
        client.dump_request_response(request, response_data, latency)

        request.data = b''
        client.dump_request_response(request, response_data, latency)

        request.data = b'test'
        client.dump_request_response(request, response_data, latency)

    def test_ask_question(self):
        arguments = MockArgumentParser()
        client = FlaskYadlanClient("yadlan", arguments)
        self.assertIsNotNone(client)
        client.configuration.client_configuration._debug = True

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890", "utterance": "Hello"}'

        response, _ = client.process_request(request)
        self.assertIsNotNone(response)
        self.assertEqual("1234567890", response['userId'])
        self.assertEqual("Hello.", response['utterance'])
        self.assertEqual("", response['response'])

    def test_process_debug_request_variables_name(self):
        home_dir = os.path.dirname(__file__) + os.sep + "testdata"
        tmp_dir = home_dir + os.sep + "tmp"
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        self.assertFalse(os.path.exists(tmp_dir))

        config_file = home_dir + os.sep + "config.yaml"
        arguments = MockArgumentParser(config=config_file)
        client = FlaskYadlanClient("testrest", arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890", "utterance": "Hello"}'
        client.process_request(request)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890", "variables": [{"type": "name", "key": "testname", "value": "value1"}]}'

        debugInfo, status = client.process_debug_request(request)
        self.assertEqual(5, len(debugInfo))
        self.assertEqual(200, status)

        self.assertEqual("value1", debugInfo['conversations']['properties']['testname'])

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        self.assertFalse(os.path.exists(tmp_dir))

    def test_process_debug_request_variables_data(self):
        home_dir = os.path.dirname(__file__) + os.sep + "testdata"
        tmp_dir = home_dir + os.sep + "tmp"
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        self.assertFalse(os.path.exists(tmp_dir))

        config_file = home_dir + os.sep + "config.yaml"
        arguments = MockArgumentParser(config=config_file)
        client = FlaskYadlanClient("testrest", arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890", "utterance": "Hello"}'
        client.process_request(request)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890", "variables": [{"type": "data", "key": "testdata", "value": "value1"}]}'

        debugInfo, status = client.process_debug_request(request)
        self.assertEqual(5, len(debugInfo))
        self.assertEqual(200, status)

        self.assertEqual("value1", debugInfo['conversations']['data_properties']['testdata'])

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        self.assertFalse(os.path.exists(tmp_dir))

    def test_process_debug_request_variables_multi(self):
        home_dir = os.path.dirname(__file__) + os.sep + "testdata"
        tmp_dir = home_dir + os.sep + "tmp"
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        self.assertFalse(os.path.exists(tmp_dir))

        config_file = home_dir + os.sep + "config.yaml"
        arguments = MockArgumentParser(config=config_file)
        client = FlaskYadlanClient("testrest", arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890", "utterance": "Hello"}'
        client.process_request(request)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890", "variables": [{"type": "name", "key": "testname", "value": "value1"}, {"type": "data", "key": "testdata", "value": "value2"}]}'

        debugInfo, status = client.process_debug_request(request)
        self.assertEqual(5, len(debugInfo))
        self.assertEqual(200, status)

        self.assertEqual("value1", debugInfo['conversations']['properties']['testname'])
        self.assertEqual("value2", debugInfo['conversations']['data_properties']['testdata'])

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        self.assertFalse(os.path.exists(tmp_dir))

    def test_process_debug_request_no_conversation(self):
        arguments = MockArgumentParser()
        client = FlaskYadlanClient("yadlan", arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890", "variables": [{"type": "name", "key": "testname", "value": "value1"}]}'

        debugInfo, status = client.process_debug_request(request)
        self.assertEqual(0, len(debugInfo))
        self.assertEqual(200, status)

    def test_process_debug_request_not_server_mode(self):
        home_dir = os.path.dirname(__file__) + os.sep + "testdata"
        tmp_dir = home_dir + os.sep + "tmp"
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        self.assertFalse(os.path.exists(tmp_dir))

        config_file = home_dir + os.sep + "config.yaml"
        arguments = MockArgumentParser(config=config_file)
        client = FlaskYadlanClient("testrest", arguments)
        client._server_mode = False
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890", "utterance": "Hello"}'
        client.process_request(request)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890", "variables": [{"type": "name", "key": "testname", "value": "value1"}]}'

        debugInfo, status = client.process_debug_request(request)
        self.assertEqual(4, len(debugInfo))
        self.assertEqual(200, status)

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        self.assertFalse(os.path.exists(tmp_dir))

    def test_process_debug_request_invalid_variables_type(self):
        arguments = MockArgumentParser()
        client = FlaskYadlanClient("yadlan", arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890", "variables": [{"type": "var", "key": "testvar", "value": "value1"}]}'

        debugInfo, status = client.process_debug_request(request)
        self.assertEqual('Invalid variables list format', debugInfo['error'])
        self.assertEqual(400, status)

    def test_process_debug_request_invalid_variables_parameter(self):
        arguments = MockArgumentParser()
        client = FlaskYadlanClient("yadlan", arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "1234567890", "variables": [{"var": "test", "value": "value1"}]}'

        debugInfo, status = client.process_debug_request(request)
        self.assertEqual('Invalid variables list format', debugInfo['error'])
        self.assertEqual(400, status)

    def test_process_debug_request(self):
        home_dir = os.path.dirname(__file__) + os.sep + "testdata"
        tmp_dir = home_dir + os.sep + "tmp"
        errors_file = tmp_dir + os.sep + "errors.txt"
        duplicates_file = tmp_dir + os.sep + "duplicates.txt"
        conversation_file = tmp_dir + os.sep + "testrest_testUser.conv"
        logs_file = tmp_dir + os.sep + "testrest_testUser.log"
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        self.assertFalse(os.path.exists(tmp_dir))

        config_file = home_dir + os.sep + "config.yaml"
        arguments = MockArgumentParser(config=config_file)
        client = FlaskYadlanClient("testrest", arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "testUser", "utterance": "Hello"}'

        response, _ = client.process_request(request)
        self.assertIsNotNone(response)
        self.assertEqual("testUser", response['userId'])
        self.assertEqual("Hello.", response['utterance'])
        self.assertEqual("HELLO, WORLD.", response['response'])

        self.assertTrue(os.path.exists(errors_file))
        self.assertTrue(os.path.exists(duplicates_file))
        self.assertTrue(os.path.exists(conversation_file))
        self.assertTrue(os.path.exists(logs_file))

        request = unittest.mock.Mock()
        request.data = b'{"userId": "testUser"}'

        debug_info, _ = client.process_debug_request(request)
        self.assertTrue('errors' in debug_info)
        self.assertTrue('duplicates' in debug_info)
        self.assertTrue('conversations' in debug_info)
        self.assertTrue('logs' in debug_info)
        self.assertTrue('current_conversation' in debug_info)

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        self.assertFalse(os.path.exists(tmp_dir))

    def test_process_debug_request_with_logs(self):
        home_dir = os.path.dirname(__file__) + os.sep + "testdata"
        tmp_dir = home_dir + os.sep + "tmp"
        errors_file = tmp_dir + os.sep + "errors.txt"
        duplicates_file = tmp_dir + os.sep + "duplicates.txt"
        conversation_file = tmp_dir + os.sep + "testrest_testUser.conv"
        logs_file = tmp_dir + os.sep + "testrest_testUser.log"
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        self.assertFalse(os.path.exists(tmp_dir))

        config_file = home_dir + os.sep + "config.yaml"
        arguments = MockArgumentParser(config=config_file)
        client = FlaskYadlanClient("testrest", arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "testUser", "utterance": "LOGS"}'

        response, _ = client.process_request(request)
        self.assertIsNotNone(response)
        self.assertEqual("testUser", response['userId'])
        self.assertEqual("LOGS.", response['utterance'])
        self.assertEqual("Output log.", response['response'])

        self.assertTrue(os.path.exists(errors_file))
        self.assertTrue(os.path.exists(duplicates_file))
        self.assertTrue(os.path.exists(conversation_file))
        self.assertTrue(os.path.exists(logs_file))

        request = unittest.mock.Mock()
        request.data = b'{"userId": "testUser"}'

        debug_info, _ = client.process_debug_request(request)
        self.assertTrue('errors' in debug_info)
        self.assertTrue('duplicates' in debug_info)
        self.assertTrue('conversations' in debug_info)
        self.assertTrue('logs' in debug_info)
        self.assertTrue('current_conversation' in debug_info)

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        self.assertFalse(os.path.exists(tmp_dir))

    def test_process_debug_request_with_variables(self):
        home_dir = os.path.dirname(__file__) + os.sep + "testdata"
        tmp_dir = home_dir + os.sep + "tmp"
        errors_file = tmp_dir + os.sep + "errors.txt"
        duplicates_file = tmp_dir + os.sep + "duplicates.txt"
        conversation_file = tmp_dir + os.sep + "testrest_testUser.conv"
        logs_file = tmp_dir + os.sep + "testrest_testUser.log"
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        self.assertFalse(os.path.exists(tmp_dir))

        config_file = home_dir + os.sep + "config.yaml"
        arguments = MockArgumentParser(config=config_file)
        client = FlaskYadlanClient("testrest", arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "testUser", "utterance": "VARIABLES"}'

        response, _ = client.process_request(request)
        self.assertIsNotNone(response)
        self.assertEqual("testUser", response['userId'])
        self.assertEqual("VARIABLES.", response['utterance'])
        self.assertEqual("Variable datas.", response['response'])

        self.assertTrue(os.path.exists(errors_file))
        self.assertTrue(os.path.exists(duplicates_file))
        self.assertTrue(os.path.exists(conversation_file))
        self.assertTrue(os.path.exists(logs_file))

        request = unittest.mock.Mock()
        request.data = b'{"userId": "testUser"}'

        debug_info, _ = client.process_debug_request(request)
        self.assertTrue('errors' in debug_info)
        self.assertTrue('duplicates' in debug_info)
        self.assertTrue('conversations' in debug_info)
        self.assertTrue('logs' in debug_info)
        self.assertTrue('current_conversation' in debug_info)

        self.assertEqual("name_value", debug_info['conversations']['properties']['name_key'])
        self.assertEqual("data_value", debug_info['conversations']['data_properties']['data_key'])
        question = debug_info['conversations']['questions'][0]
        self.assertEqual("var_value", question['var_properties']['var_key'])

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        self.assertFalse(os.path.exists(tmp_dir))

    def test_process_debug_request_no_userid(self):
        home_dir = os.path.dirname(__file__) + os.sep + "testdata"
        tmp_dir = home_dir + os.sep + "tmp"
        errors_file = tmp_dir + os.sep + "errors.txt"
        duplicates_file = tmp_dir + os.sep + "duplicates.txt"
        conversation_file = tmp_dir + os.sep + "testrest_testUser.conv"
        logs_file = tmp_dir + os.sep + "testrest_testUser.log"
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        self.assertFalse(os.path.exists(tmp_dir))

        config_file = home_dir + os.sep + "config.yaml"
        arguments = MockArgumentParser(config=config_file)
        client = FlaskYadlanClient("testrest", arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.data = b'{"userId": "testUser", "utterance": "Hello"}'

        response, _ = client.process_request(request)
        self.assertIsNotNone(response)
        self.assertEqual("testUser", response['userId'])
        self.assertEqual("Hello.", response['utterance'])
        self.assertEqual("HELLO, WORLD.", response['response'])

        self.assertTrue(os.path.exists(errors_file))
        self.assertTrue(os.path.exists(duplicates_file))
        self.assertTrue(os.path.exists(conversation_file))
        self.assertTrue(os.path.exists(logs_file))

        request = unittest.mock.Mock()
        request.data = b'{}'

        debug_info, _ = client.process_debug_request(request)
        self.assertTrue('errors' in debug_info)
        self.assertTrue('duplicates' in debug_info)
        self.assertFalse('conversations' in debug_info)
        self.assertFalse('logs' in debug_info)
        self.assertFalse('current_conversation' in debug_info)

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        self.assertFalse(os.path.exists(tmp_dir))
