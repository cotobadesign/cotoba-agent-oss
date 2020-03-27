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

from programy.extensions.geocode.geocode import GeoCodeExtension
from programy.utils.geo.google import GoogleMaps

from programytest.client import TestClient


class MockGoogleMaps(GoogleMaps):

    def __init__(self, data_file_name):
        self._data_file_name = data_file_name

    def _get_response_as_json(self, url):
        with open(self._data_file_name, "r", encoding="utf-8") as data_file:
            return json.load(data_file)


class MockGeoCodeExtension(GeoCodeExtension):

    def get_geo_locator(self):
        return MockGoogleMaps(GeoCodeAIMLTests.LATLONG)


class GeoCodeTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_storage(self):
        super(GeoCodeTestsClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class GeoCodeAIMLTests(unittest.TestCase):

    LATLONG = None

    def setUp(self):
        client = GeoCodeTestsClient()
        self._client_context = client.create_client_context("testid")

    def test_postcode1(self):
        GeoCodeAIMLTests.LATLONG = os.path.dirname(__file__) + os.sep + "google_latlong.json"
        self.assertTrue(os.path.exists(GeoCodeAIMLTests.LATLONG))
        response = self._client_context.bot.ask_question(self._client_context, "POSTCODE KY39UR")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'LATITUDE DEC 56 FRAC 0720397 LONGITUDE DEC -3 FRAC 1752001.')

    def test_postcode2(self):
        GeoCodeAIMLTests.LATLONG = os.path.dirname(__file__) + os.sep + "google_latlong.json"
        self.assertTrue(os.path.exists(GeoCodeAIMLTests.LATLONG))
        response = self._client_context.bot.ask_question(self._client_context, "POSTCODE KY3 9UR")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'LATITUDE DEC 56 FRAC 0720397 LONGITUDE DEC -3 FRAC 1752001.')

    def test_location(self):
        GeoCodeAIMLTests.LATLONG = os.path.dirname(__file__) + os.sep + "google_latlong.json"
        self.assertTrue(os.path.exists(GeoCodeAIMLTests.LATLONG))
        response = self._client_context.bot.ask_question(self._client_context, "LOCATION KINGHORN")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'LATITUDE DEC 56 FRAC 0720397 LONGITUDE DEC -3 FRAC 1752001.')
