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


class PatternOrderingTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(PatternOrderingTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])
        self.add_sets_store([os.path.dirname(__file__) + os.sep + "sets"])


class PatternOrderingAIMLTests(unittest.TestCase):

    def setUp(self):
        client = PatternOrderingTestClient()
        self._client_context = client.create_client_context("testid")

    def test_basic_no_match(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE COLOR IS BLUE")
        self.assertEqual(response, "I didn't recognize BLUE AS A COLOR.")

    def test_basic_match(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE COLOR IS RED")
        self.assertEqual(response, "Red IS A NICE COLOR.")

    def test_basic_exact_match(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE COLOR IS GREEN")
        self.assertEqual(response, "Green IS MY FAVORITE COLOR TOO!")

    def test_hash_v_star(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE ANIMAL IS A DOLPHIN")
        self.assertEqual(response, "HASH SELECTED.")

        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE ANIMAL IS AN AARDVARK")
        self.assertEqual(response, "SELECTED ONCE.")
