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

from programy.utils.geo.geonames import GeoNamesApi
from programy.utils.license.keys import LicenseKeys


class GeoNamesTests(unittest.TestCase):

    def setUp(self):
        self.license_keys = LicenseKeys()
        self.license_keys.load_license_key_file(os.path.dirname(__file__) + "/../../../../bots/y-bot/config/license.keys")

    def test_geonames(self):

        geonames = GeoNamesApi(self.license_keys)
        self.assertIsNotNone(geonames)

        latlng = geonames.get_latlong_for_postcode('KY39UR')
        self.assertIsNotNone(latlng)
        self.assertEqual(latlng.latitude, 56.07206267570594)
        self.assertEqual(latlng.longitude, -3.175233048730664)
