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
import json

from programy.extensions.maps.maps import GoogleMapsExtension
from programy.utils.geo.google import GoogleMaps

from programytest.client import TestClient


class MockGoogleMaps(GoogleMaps):

    def __init__(self, response_file):
        self._response_file = response_file

    def _get_response_as_json(self, url):
        with open(self._response_file, "r", encoding="utf-8") as response_data:
            return json.load(response_data)


class MockGoogleMapsExtension(GoogleMapsExtension):

    response_file = None

    def get_geo_locator(self):
        return MockGoogleMaps(MockGoogleMapsExtension.response_file)


class MapsTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_storage(self):
        super(MapsTestsClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class MapsAIMLTests(unittest.TestCase):

    def setUp(self):
        client = MapsTestsClient()
        self._client_context = client.create_client_context("testid")

    def test_distance(self):
        MockGoogleMapsExtension.response_file = os.path.dirname(__file__) + os.sep + "distance.json"

        response = self._client_context.bot.ask_question(self._client_context, "DISTANCE EDINBURGH KINGHORN")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'It is 25 . 1 miles.')

    def test_directions(self):
        MockGoogleMapsExtension.response_file = os.path.dirname(__file__) + os.sep + "directions.json"

        response = self._client_context.bot.ask_question(self._client_context, "DIRECTIONS EDINBURGH KINGHORN")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("To get there Head west on Leith St"))
