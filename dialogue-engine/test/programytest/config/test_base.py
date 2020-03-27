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

from programy.config.base import BaseConfigurationData


class BaseConfigurationDataTests(unittest.TestCase):

    def test_sub_bot_root(self):
        config = BaseConfigurationData("test")

        replaced = config.sub_bot_root(os.sep + "data",  os.sep + "root")
        self.assertIsNotNone(replaced)
        self.assertEqual(replaced,  os.sep + "data")

        replaced = config.sub_bot_root("$BOT_ROOT" + os.sep + "data",  os.sep + "root")
        self.assertIsNotNone(replaced)
        self.assertEqual(replaced,  os.sep + "root" + os.sep + "data")

        replaced = config.sub_bot_root("$BOT_ROOT$BOT_ROOT" + os.sep + "data",  os.sep + "root")
        self.assertIsNotNone(replaced)
        self.assertEqual(replaced,  os.sep + "root" + os.sep + "root" + os.sep + "data")

    def test_additionals(self):
        config = BaseConfigurationData("test")

        self.assertEqual([], config.additionals_to_add())

        config._additionals["key1"] = "value1"
        config._additionals["key2"] = "value2"

        self.assertTrue(config.exists("key1"))
        self.assertEqual("value1", config.value("key1"))

        self.assertTrue(config.exists("key2"))
        self.assertEqual("value2", config.value("key2"))

        self.assertFalse(config.exists("key3"))
