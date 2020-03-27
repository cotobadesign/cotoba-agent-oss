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

from programy.config.file.file import BaseConfigurationFile
from programy.utils.substitutions.substitues import Substitutions


class TestBaseConfigurationFile(BaseConfigurationFile):

    def load_from_text(self, text, client_configuration, bot_root):
        return None

    def load_from_file(self, filename, client_configuration, bot_root):
        return None

    def get_section(self, section_name, parent_section=None):
        return None

    def get_section_data(self, section_name, parent_section=None):
        return None

    def get_child_section_keys(self, section_name, parent_section=None):
        return None

    def get_option(self, section, option_name, missing_value=None, subs: Substitutions = None):
        return None


class BaseConfigurationFileTests(unittest.TestCase):

    def test_convert_to_bool(self):
        config = TestBaseConfigurationFile()

        self.assertTrue(config.convert_to_bool("true"))
        self.assertTrue(config.convert_to_bool("True"))
        self.assertTrue(config.convert_to_bool("TRUE"))

        self.assertFalse(config.convert_to_bool("false"))
        self.assertFalse(config.convert_to_bool("False"))
        self.assertFalse(config.convert_to_bool("FALSE"))

        with self.assertRaises(Exception):
            config.convert_to_bool("")

        with self.assertRaises(Exception):
            config.convert_to_bool("XXX")

    def test_convert_to_int(self):
        config = TestBaseConfigurationFile()

        self.assertEqual(0, config.convert_to_int('0'))
        self.assertEqual(10, config.convert_to_int('10'))

        with self.assertRaises(Exception):
            config.convert_to_int("")

        with self.assertRaises(Exception):
            config.convert_to_int("XXX")
