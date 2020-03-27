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
from programy.config.brain.nlu import BrainNluConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class BrainNluConfigurationTests(unittest.TestCase):

    def test_nlu_default(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            nlu:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        nlu_config = BrainNluConfiguration()
        nlu_config.load_config_section(yaml, brain_config, "nlu")

        self.assertEqual("programy.nlu.nlu.NluRequest", nlu_config.classname)
        self.assertEqual("http://localhost:3000/run", nlu_config.url)
        self.assertEqual("", nlu_config.apikey)

    def test_nlu_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            nlu:
                classname: programy.nlu.nlu.TestNluRequest
                url: http://TestNlu
                apikey: xxxxx
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        nlu_config = BrainNluConfiguration()
        nlu_config.load_config_section(yaml, brain_config, "nlu")

        self.assertEqual("programy.nlu.nlu.TestNluRequest", nlu_config.classname)
        self.assertEqual("http://TestNlu", nlu_config.url)
        self.assertEqual("xxxxx", nlu_config.apikey)
