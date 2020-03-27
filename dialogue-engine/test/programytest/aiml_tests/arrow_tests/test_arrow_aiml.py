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


class ArrowTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(ArrowTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class ArrowAIMLTests(unittest.TestCase):

    def setUp(self):
        client = ArrowTestClient()
        self._client_context = client.create_client_context("testid")

    def test_arrow_first_word(self):
        response = self._client_context.bot.ask_question(self._client_context,  "SAY HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS SAY.')

    def test_arrow_first_no_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS.')

    def test_arrow_first_multi_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "WE SAY HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS WE SAY.')

    def test_arrow_first_multi_match(self):
        response = self._client_context.bot.ask_question(self._client_context, "WE CHECKING MULTI WORD MATCH")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS NOW WE.')

    def test_arrow_last_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO YOU")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS YOU.')

    def test_arrow_no_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS.')

    def test_arrow_no_multi_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO YOU THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS YOU THERE.')

    def test_arrow_middle_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL HI THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS HI.')

    def test_arrow_middle_no_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS.')

    def test_arrow_middle_multi_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL I WAS THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS I WAS.')

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
