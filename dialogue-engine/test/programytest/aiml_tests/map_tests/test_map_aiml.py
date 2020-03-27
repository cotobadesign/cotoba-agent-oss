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


class MapAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(MapAIMLTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class MapAIMLTests(unittest.TestCase):

    def setUp(self):
        client = MapAIMLTestClient()
        self._client_context = client.create_client_context("testid")

        self._client_context.brain.properties.load_from_text("""
             default-get:unknown
         """)
        self._client_context.bot.brain.dynamics.add_dynamic_map('romantodec', "programy.dynamic.maps.roman.MapRomanToDecimal", None)
        self._client_context.bot.brain.dynamics.add_dynamic_map('dectoroman', "programy.dynamic.maps.roman.MapDecimalToRoman", None)
        self._client_context.bot.brain.maps.add_map("testmap", {"1": "One", "2": "Two", "3": "Three"}, "file")

    def test_static_map(self):
        response = self._client_context.bot.ask_question(self._client_context,  "STATIC MAP TEST")
        self.assertEqual(response, "One.")

    def test_plural_map(self):
        response = self._client_context.bot.ask_question(self._client_context,  "PLURAL MAP TEST")
        self.assertEqual(response, "TWOS.")

    def test_singular_map(self):
        response = self._client_context.bot.ask_question(self._client_context,  "SINGULAR MAP TEST")
        self.assertEqual(response, "TWO.")

    def test_successor_map(self):
        response = self._client_context.bot.ask_question(self._client_context,  "SUCCESSOR MAP TEST")
        self.assertEqual(response, "667.")

    def test_predessor_map(self):
        response = self._client_context.bot.ask_question(self._client_context,  "PREDECESSOR MAP TEST")
        self.assertEqual(response, "666.")

    def test_dynamic_map(self):
        response = self._client_context.bot.ask_question(self._client_context,  "DYNAMIC MAP DECIMAL TO ROMAN")
        self.assertEqual(response, "20 is XX.")

        response = self._client_context.bot.ask_question(self._client_context,  "DYNAMIC MAP ROMAN TO DECIMAL")
        self.assertEqual(response, "XX is 20.")
