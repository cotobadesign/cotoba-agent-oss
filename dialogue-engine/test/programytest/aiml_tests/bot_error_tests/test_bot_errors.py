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

from programytest.client import TestClient


class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(BasicTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class BasicAIMLTests(unittest.TestCase):

    def setUp(self):
        client = BasicTestClient()
        self._client_context = client.create_client_context("testid")

    def test_bot_error_over_srai_loop(self):
        self._client_context.bot.configuration._max_search_srai = 5
        response = self._client_context.bot.ask_question(self._client_context, "SRAI OVER")
        self.assertEqual(response, '')
        conversation = self._client_context.bot.conversation(self._client_context)
        self.assertEqual(conversation.exception, 'Max search srai [5] exceeded: [SRAI LOOP-2]')

    def test_bot_error_over_srai_loop_with_default_response(self):
        self._client_context.bot.configuration._max_search_srai = 5
        self._client_context.brain.properties.add_property("exception-response", "Limit over")
        response = self._client_context.bot.ask_question(self._client_context, "SRAI OVER")
        self.assertEqual(response, 'Limit over.')
        conversation = self._client_context.bot.conversation(self._client_context)
        self.assertEqual(conversation.exception, 'Max search srai [5] exceeded: [SRAI LOOP-2]')

    def test_bot_error_over_condition_type2_loop(self):
        self._client_context.bot.configuration._max_search_condition = 5
        response = self._client_context.bot.ask_question(self._client_context, "CONDITION TYPE2 OVER")
        self.assertEqual(response, '')
        conversation = self._client_context.bot.conversation(self._client_context)
        self.assertEqual(conversation.exception, 'Max search condition [5] exceeded: [CONDITION var="test" value=default]')

    def test_bot_error_over_condition_type3_loop(self):
        self._client_context.bot.configuration._max_search_condition = 5
        response = self._client_context.bot.ask_question(self._client_context, "CONDITION TYPE3 OVER")
        self.assertEqual(response, '')
        conversation = self._client_context.bot.conversation(self._client_context)
        self.assertEqual(conversation.exception, 'Max search condition [5] exceeded: [CONDITION default]')
