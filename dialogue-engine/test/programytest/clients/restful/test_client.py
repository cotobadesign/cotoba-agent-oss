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

from programy.clients.restful.client import RestBotClient
from programy.clients.restful.config import RestConfiguration

from programytest.clients.arguments import MockArgumentParser


class RestBotClientTests(unittest.TestCase):

    def test_init(self):
        arguments = MockArgumentParser()
        client = RestBotClient("testrest", arguments)
        self.assertIsNotNone(client)
        self.assertIsNotNone(client.get_client_configuration())
        self.assertIsInstance(client.get_client_configuration(), RestConfiguration)
        self.assertEqual([], client.api_keys)

        request = unittest.mock.Mock()
        client.process_request(request)

    def test_api_keys(self):
        arguments = MockArgumentParser()
        client = RestBotClient("testrest", arguments)
        self.assertIsNotNone(client)

        client.configuration.client_configuration._use_api_keys = True
        client.configuration.client_configuration._api_key_file = os.path.dirname(__file__) + os.sep + ".." + os.sep + "api_keys.txt"

        client.load_api_keys()

        self.assertEqual(3, len(client.api_keys))
        self.assertTrue(client.is_apikey_valid("11111111"))
        self.assertTrue(client.is_apikey_valid("22222222"))
        self.assertTrue(client.is_apikey_valid("33333333"))
        self.assertFalse(client.is_apikey_valid("99999999"))
