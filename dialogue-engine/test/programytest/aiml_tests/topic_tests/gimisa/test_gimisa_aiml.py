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


class GimisaTopicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(GimisaTopicTestClient, self).load_storage()
        self.add_default_stores()
        self.add_single_categories_store(os.path.dirname(__file__) + os.sep + "gimisa_test.aiml")
        self.add_sets_store([os.path.dirname(__file__) + os.sep + "sets"])
        self.add_maps_store([os.path.dirname(__file__) + os.sep + "maps"])


class GimisaAIMLTests(unittest.TestCase):

    def setUp(self):
        client = GimisaTopicTestClient()
        self._client_context = client.create_client_context("testid")

    def test_ask_blender_twice(self):
        response = self._client_context.bot.ask_question(self._client_context, "render")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Some definition of render as per professor ....')

        response = self._client_context.bot.ask_question(self._client_context, "hello")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Hi .. setting topic to blender....')

        response = self._client_context.bot.ask_question(self._client_context, "render")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'The definition of render in blender is mixing.')
