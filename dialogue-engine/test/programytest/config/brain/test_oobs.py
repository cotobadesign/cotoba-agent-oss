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

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.brain.oobs import BrainOOBSConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class BrainOOBsConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            oob:
              default:
                classname: programy.oob.defaults.default.DefaultOutOfBandProcessor
              dial:
                classname: programy.oob.defaults.dial.DialOutOfBandProcessor
              email:
                classname: programy.oob.defaults.email.EmailOutOfBandProcessor
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        oobs_config = BrainOOBSConfiguration()
        oobs_config.load_config_section(yaml, brain_config, ".")

        self.assertTrue(oobs_config.exists("default"))
        self.assertTrue(oobs_config.exists("dial"))
        self.assertTrue(oobs_config.exists("email"))
        self.assertFalse(oobs_config.exists("Other"))

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            oobs:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        oobs_config = BrainOOBSConfiguration()
        oobs_config.load_config_section(yaml, brain_config, ".")

        self.assertFalse(oobs_config.exists("default"))
        self.assertFalse(oobs_config.exists("dial"))
        self.assertFalse(oobs_config.exists("email"))
        self.assertFalse(oobs_config.exists("Other"))

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        oobs_config = BrainOOBSConfiguration()
        oobs_config.load_config_section(yaml, brain_config, ".")

        self.assertFalse(oobs_config.exists("default"))
        self.assertFalse(oobs_config.exists("dial"))
        self.assertFalse(oobs_config.exists("email"))
        self.assertFalse(oobs_config.exists("Other"))
