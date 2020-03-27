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


class HashAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(HashAIMLTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class HashAIMLTests(unittest.TestCase):

    def setUp(self):
        client = HashAIMLTestClient()
        self._client_context = client.create_client_context("testid")

    def test_hash_first_word(self):
        response = self._client_context.bot.ask_question(self._client_context,  "SAY HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS SAY.')

    def test_hash_first_no_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS.')

    def test_hash_first_multi_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "WE SAY HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS WE SAY.')

    def test_hash_last_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO YOU")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS YOU.')

    def test_hash_no_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS.')

    def test_hash_no_multi_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO YOU THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS YOU THERE.')

    def test_hash_middle_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL HI THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS HI.')

    def test_hash_middle_no_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS.')

    def test_hash_middle_multi_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL I WAS THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS I WAS.')

    def test_hash_middle_and_end(self):
        response = self._client_context.bot.ask_question(self._client_context, "ARE YOU FUN")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'I AM FUNNY.')

        response = self._client_context.bot.ask_question(self._client_context, "DO FUN YOU")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'I AM FUNNY.')

    def test_test1_testx_issue(self):
        response = self._client_context.bot.ask_question(self._client_context, "TEST1 TESTX")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Answer 1.')

    def test_test1_test2_issue(self):
        response = self._client_context.bot.ask_question(self._client_context, "TEST1 TEST2")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Answer 2.')

    def test_test3_issue(self):
        response = self._client_context.bot.ask_question(self._client_context, "TEST3")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Answer 3.')

    def test_test1_issue(self):
        response = self._client_context.bot.ask_question(self._client_context, "TEST1")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Answer 1.')
