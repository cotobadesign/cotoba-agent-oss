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


class PatternSetTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(PatternSetTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])
        self.add_sets_store([os.path.dirname(__file__) + os.sep + "sets"])


class PatternSetAIMLTests(unittest.TestCase):

    def setUp(self):
        client = PatternSetTestClient()
        self._client_context = client.create_client_context("testid")

        self._client_context.brain.dynamics.add_dynamic_set('number', "programy.dynamic.sets.numeric.IsNumeric", None)

    def test_patten_set_match(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE COLOR IS AMBER")
        self.assertEqual(response, "Amber IS A NICE COLOR.")

    def test_patten_match_multi_word_set(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE COLOR IS AIR FORCE BLUE")
        self.assertEqual(response, "Air Force blue IS A NICE COLOR.")

    def test_patten_match_multi_word_set_latina(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE COLOR IS CAFÉ AU LAIT")
        self.assertEqual(response, "Café au lait IS A NICE COLOR.")

    def test_patten_match_mixed_word_set(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE COLOR IS RED")

        self.assertEqual(response, "Red IS A NICE COLOR.")

        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE COLOR IS RED ORANGE")
        self.assertEqual(response, "Red Orange IS A NICE COLOR.")

        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE COLOR IS SACRAMENTO STATE GREEN")
        self.assertEqual(response, "Sacramento State green IS A NICE COLOR.")

    def test_patten_match_mixed_word_set_longer_sentence(self):
        response = self._client_context.bot.ask_question(self._client_context,  "I DO NOT LIKE RED VERY MUCH")
        self.assertEqual(response, "IT IS OK, Red IS NOT MY BEST COLOUR EITHER.")

        response = self._client_context.bot.ask_question(self._client_context,  "I DO NOT LIKE RED ORANGE AT ALL")
        self.assertEqual(response, "IT IS OK, Red Orange IS NOT MY BEST COLOUR EITHER.")

        response = self._client_context.bot.ask_question(self._client_context,  "I DO NOT LIKE SACRAMENTO STATE GREEN AT ALL")
        self.assertEqual(response, "IT IS OK, Sacramento State green IS NOT MY BEST COLOUR EITHER.")

    def test_patten_match_mixed_word_set_at_front(self):
        response = self._client_context.bot.ask_question(self._client_context,  "RED IS A NICE COLOUR")
        self.assertEqual(response, "YES Red IS A LOVELY COLOUR.")

        response = self._client_context.bot.ask_question(self._client_context,  "RED ORANGE IS A NICE COLOUR")
        self.assertEqual(response, "YES Red Orange IS A LOVELY COLOUR.")

        response = self._client_context.bot.ask_question(self._client_context,  "SACRAMENTO STATE GREEN IS A NICE COLOUR")
        self.assertEqual(response, "YES Sacramento State green IS A LOVELY COLOUR.")

    def test_inbuilt_set_number(self):
        response = self._client_context.bot.ask_question(self._client_context,  "Is 666 a number")
        self.assertEqual(response, "Yes 666 is a number.")
