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
import os

from programy.utils.substitutions.substitues import Substitutions

from programytest.client import TestClient


class HashUDCTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(HashUDCTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])

    def load_configuration(self, arguments, subs: Substitutions = None):
        super(HashUDCTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0]._empty_string = "YEMPTY"


class UDCAIMLTests(unittest.TestCase):

    def setUp(self):
        client = HashUDCTestClient()
        self._client_context = client.create_client_context("testid")

    def test_udc_multi_word_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "Ask Question")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC Hash Response.")

    def test_udc_single_word_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "Question")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC Hash Response.")

    def test_udc_empty_string_question1(self):
        response = self._client_context.bot.ask_question(self._client_context, "YEMPTY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC Hash Response.")

    def test_udc_empty_string_question2(self):
        response = self._client_context.bot.ask_question(self._client_context, "")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC Hash Response.")
