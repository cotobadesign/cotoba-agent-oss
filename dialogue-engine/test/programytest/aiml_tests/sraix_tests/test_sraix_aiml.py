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

from programytest.client import TestClient
from programy.services.service import Service
from programy.config.brain.service import BrainServiceConfiguration
from programy.services.service import ServiceFactory


class SraixTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(SraixTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class MockGenericRESTService(Service):

    def __init__(self, config: BrainServiceConfiguration):
        Service.__init__(self, config)

    def ask_question(self, client_context, question: str):
        return "ANSWER"


class SraixAIMLTests(unittest.TestCase):

    def setUp(self):
        client = SraixTestClient()
        self._client_context = client.create_client_context("testid")

        config = unittest.mock.Mock()
        ServiceFactory.services['REST'] = MockGenericRESTService(config)

    def test_basic_sraix_test(self):
        response = self._client_context.bot.ask_question(self._client_context, "GENERIC REST TEST")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ANSWER.')

    def test_unknown_sraix_test(self):
        response = self._client_context.bot.ask_question(self._client_context, "UNKNOWN REST TEST")
        self.assertIsNotNone(response)
        self.assertEqual(response, '')
