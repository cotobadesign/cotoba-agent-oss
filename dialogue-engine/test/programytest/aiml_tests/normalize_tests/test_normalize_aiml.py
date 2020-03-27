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


class NormalizeTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(NormalizeTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])
        self.add_normal_store(os.path.dirname(__file__) + os.sep + "normal.txt")


class NormalizeAIMLTests(unittest.TestCase):

    def setUp(self):
        client = NormalizeTestClient()
        self._client_context = client.create_client_context("testid")

    def test_normalize(self):
        response = self._client_context.bot.ask_question(self._client_context,  "TEST NORMALIZE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Keithsterling dot com.")

    def test_normalize_star(self):
        response = self._client_context.bot.ask_question(self._client_context,  "NORMALIZE test.org", srai=True)
        self.assertIsNotNone(response)
        self.assertEqual(response, "Test dot org")
