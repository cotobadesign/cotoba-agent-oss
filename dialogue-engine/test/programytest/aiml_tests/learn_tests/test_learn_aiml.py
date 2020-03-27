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


class LearnTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(LearnTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class LearnAIMLTests(unittest.TestCase):

    def setUp(self):
        client = LearnTestClient()
        self._client_context = client.create_client_context("testid")

    def test_learn(self):
        response = self._client_context.bot.ask_question(self._client_context, "MY NAME IS FRED")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK, I will remember your name is FRED.")

        response = self._client_context.bot.ask_question(self._client_context, "WHAT IS MY NAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "YOUR NAME IS FRED.")

    def test_learn_x_is_y(self):

        response = self._client_context.bot.ask_question(self._client_context, "LEARN THE SUN IS HOT")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK, I will remember THE SUN is HOT.")

        response = self._client_context.bot.ask_question(self._client_context, "LEARN THE SKY IS BLUE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK, I will remember THE SKY is BLUE.")

        response = self._client_context.bot.ask_question(self._client_context, "LEARN THE MOON IS GREY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK, I will remember THE MOON is GREY.")

        response = self._client_context.bot.ask_question(self._client_context, "WHAT IS THE SUN")
        self.assertIsNotNone(response)
        self.assertEqual(response, "HOT.")

        response = self._client_context.bot.ask_question(self._client_context, "WHAT IS THE SKY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "BLUE.")

        response = self._client_context.bot.ask_question(self._client_context, "WHAT IS THE MOON")
        self.assertIsNotNone(response)
        self.assertEqual(response, "GREY.")

    def test_base_aiml_category_over_learn(self):
        self._client_context.brain.bot.configuration._max_categories = 4

        response = self._client_context.bot.ask_question(self._client_context, "LEARN THE SUN IS HOT")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK, I will remember THE SUN is HOT.")

        response = self._client_context.bot.ask_question(self._client_context, "LEARN THE SKY IS BLUE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "")

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertEqual("Max categories [4] exceeded: [WHAT IS THE SKY]", conversation._exception)

    def test_base_aiml_category_replace_learn(self):
        self._client_context.brain.bot.configuration._max_categories = 4

        response = self._client_context.bot.ask_question(self._client_context, "LEARN THE SUN IS HOT")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK, I will remember THE SUN is HOT.")

        response = self._client_context.bot.ask_question(self._client_context, "LEARN THE SUN IS HOT")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK, I will remember THE SUN is HOT.")
