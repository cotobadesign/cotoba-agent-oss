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


class PatternISetTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(PatternISetTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class PatternISetAIMLTests(unittest.TestCase):

    def setUp(self):
        client = PatternISetTestClient()
        self._client_context = client.create_client_context("testid")

    def test_patten_set_match(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE COLOR IS RED")
        self.assertEqual(response, "RED IS A NICE COLOR.")

        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE COLOR IS GREEN")
        self.assertEqual(response, "")

    def test_patten_set_one_or_more_wildcard_match(self):
        response = self._client_context.bot.ask_question(self._client_context,  "WHAT IS YOUR FAVOURITE COLOUR PLEASE")
        self.assertEqual(response, "My favourite colour is Red.")

        response = self._client_context.bot.ask_question(self._client_context,  "WHAT IS YOUR FAVOURITE COLOR PLEASE")
        self.assertEqual(response, "My favourite color is Red.")

    def test_patten_set_zero_or_more_wildcard_match(self):
        response = self._client_context.bot.ask_question(self._client_context,  "I LIKE TO EAT BURGERS")
        self.assertEqual(response, "Wow, I like to eat burgers too.")

        response = self._client_context.bot.ask_question(self._client_context,  "I LIKE TO MUNCH SUSHI")
        self.assertEqual(response, "Wow, I like to munch sushi too.")

        response = self._client_context.bot.ask_question(self._client_context,  "I LIKE TO CHOW FRENCH FRIES")
        self.assertEqual(response, "Wow, I like to chow french fries too.")

    def test_patten_alternative_set_match(self):
        response = self._client_context.bot.ask_question(self._client_context,  "I LIKE RIDING BMW MOTORCYCLES")
        self.assertEqual(response, "I prefer a Harley Davidson to a BMW.")

    def test_united_kingdom(self):
        response = self._client_context.bot.ask_question(self._client_context,  "I live in wales")
        self.assertEqual(response, "Thats great, I live in the UK too!")

        response = self._client_context.bot.ask_question(self._client_context,  "I live in WALES")
        self.assertEqual(response, "Thats great, I live in the UK too!")

        response = self._client_context.bot.ask_question(self._client_context,  "I live in Wales")
        self.assertEqual(response, "Thats great, I live in the UK too!")
