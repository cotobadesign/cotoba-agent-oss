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

from programy.utils.license.keys import LicenseKeys


class LicenseKeyTests(unittest.TestCase):

    def test_add_keys(self):
        keys = LicenseKeys()
        self.assertFalse(keys.has_keyVal("KEY1"))
        keys.add_key("KEY1", "VALUE1")
        self.assertTrue(keys.has_keyVal("KEY1"))
        self.assertEqual("VALUE1", keys.get_key("KEY1"))
        keys.add_key("KEY1", "VALUE2")
        self.assertTrue(keys.has_keyVal("KEY1"))
        self.assertEqual("VALUE2", keys.get_key("KEY1"))

    def test_load_license_keys_file(self):
        keys = LicenseKeys()
        keys.add_key("KEY1", "Key1Data")
        keys.add_key("KEY2", "Key2Data")
        keys.add_key("KEY3", "KEY3 Data With Spaces")

        self.assertTrue(keys.has_keyVal('KEY1'))
        self.assertEqual("Key1Data", keys.get_key("KEY1"))
        self.assertTrue(keys.has_keyVal('KEY2'))
        self.assertEqual("Key2Data", keys.get_key("KEY2"))
        self.assertTrue(keys.has_keyVal('KEY3'))
        self.assertEqual("KEY3 Data With Spaces", keys.get_key("KEY3"))
        with self.assertRaises(Exception):
            keys.get_key("KEY5")
