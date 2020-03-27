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

from programy.dynamic.maps.roman import MapDecimalToRoman
from programy.dynamic.maps.roman import MapRomanToDecimal
from programy.context import ClientContext

from programytest.client import TestClient


class IsRomanNumeralDynamicSetTests(unittest.TestCase):

    def setUp(self):
        self._client_context = ClientContext(TestClient(), "testid")

    def test_romantodec(self):
        dyn_map = MapRomanToDecimal(None)
        self.assertIsNotNone(dyn_map)
        self.assertEqual("20", dyn_map.map_value(self._client_context, "XX"))
        self.assertEqual("4", dyn_map.map_value(self._client_context, "IV"))

    def test_dectoroman(self):
        dyn_map = MapDecimalToRoman(None)
        self.assertIsNotNone(dyn_map)
        self.assertEqual("XX", dyn_map.map_value(self._client_context, "20"))
        self.assertEqual("IV", dyn_map.map_value(self._client_context, "4"))
