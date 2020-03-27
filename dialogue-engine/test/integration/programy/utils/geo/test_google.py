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

from programy.utils.geo.google import GoogleMaps, GoogleDistance, GoogleDirections
from programy.utils.geo.latlong import LatLong


class GoogleMapsTests(unittest.TestCase):

    def test_location(self):
        googlemaps = GoogleMaps(None)

        latlng = googlemaps.get_latlong_for_location("KY3 9UR")
        self.assertIsNotNone(latlng)
        self.assertIsInstance(latlng, LatLong)
        self.assertEqual(latlng.latitude, 56.0720397)
        self.assertEqual(latlng.longitude, -3.1752001)

    def test_distance_uk_driving_imperial(self):
        googlemaps = GoogleMaps(None)

        distance = googlemaps.get_distance_between_addresses("Edinburgh", "London", country="UK", mode="driving", units="imperial")
        self.assertIsNotNone(distance)
        self.assertIsInstance(distance, GoogleDistance)
        self.assertEqual("409 mi", distance._distance_text)

    def test_directions(self):
        googlemaps = GoogleMaps(None)

        directions = googlemaps.get_directions_between_addresses("Edinburgh", "London")
        self.assertIsNotNone(directions)
        self.assertIsInstance(directions, GoogleDirections)
