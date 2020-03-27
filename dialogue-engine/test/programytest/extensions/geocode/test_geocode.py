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

    def __init__(self, geo_locator):
        self._geo_locator = geo_locator

    def get_geo_locator(self):
        return self._geo_locator


class GeoCodeExtensionTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self.context = client.create_client_context("testid")

    def test_geocode_postcode1(self):
        filename = os.path.dirname(__file__) + os.sep + "google_latlong.json"
        self.assertTrue(os.path.isfile(filename))
        geo_locator = MockGoogleMaps(filename)
        self.assertIsNotNone(geo_locator)
        geocode = MockGeoCodeExtension(geo_locator)
        self.assertIsNotNone(geocode)

        result = geocode.execute(self.context, "POSTCODE1 KY39UR")
        self.assertIsNotNone(result)
        self.assertEqual("LATITUDE DEC 56 FRAC 0720397 LONGITUDE DEC -3 FRAC 1752001", result)

    def test_geocode_postcode2(self):
        filename = os.path.dirname(__file__) + os.sep + "google_latlong.json"
        self.assertTrue(os.path.isfile(filename))
        geo_locator = MockGoogleMaps(filename)
        self.assertIsNotNone(geo_locator)
        geocode = MockGeoCodeExtension(geo_locator)
        self.assertIsNotNone(geocode)

        result = geocode.execute(self.context, "POSTCODE2 KY3 9UR")
        self.assertIsNotNone(result)
        self.assertEqual("LATITUDE DEC 56 FRAC 0720397 LONGITUDE DEC -3 FRAC 1752001", result)

    def test_geocode_location(self):
        filename = os.path.dirname(__file__) + os.sep + "google_latlong.json"
        self.assertTrue(os.path.isfile(filename))
        geo_locator = MockGoogleMaps(filename)
        self.assertIsNotNone(geo_locator)
        geocode = MockGeoCodeExtension(geo_locator)
        self.assertIsNotNone(geocode)

        result = geocode.execute(self.context, "LOCATION KINGHORN")
        self.assertIsNotNone(result)
        self.assertEqual("LATITUDE DEC 56 FRAC 0720397 LONGITUDE DEC -3 FRAC 1752001", result)
