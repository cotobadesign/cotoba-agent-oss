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
from programy.config.brain.services import BrainServicesConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class BrainServicesConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            services:
                REST:
                    classname: programy.services.rest.GenericRESTService
                    method: GET
                    host: 0.0.0.0
                Pannous:
                    classname: programy.services.pannous.PannousService
                    url: http://weannie.pannous.com/api
                Pandora:
                    classname: programy.services.pandora.PandoraService
                    url: http://www.pandorabots.com/pandora/talk-xml
                Wikipedia:
                    classname: programy.services.wikipediaservice.WikipediaService
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        services_config = BrainServicesConfiguration()
        services_config.load_config_section(yaml, brain_config, ".")

        self.assertTrue(services_config.exists("REST"))
        self.assertTrue(services_config.exists("Pannous"))
        self.assertTrue(services_config.exists("Pandora"))
        self.assertTrue(services_config.exists("Wikipedia"))
        self.assertFalse(services_config.exists("Other"))

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            services:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        services_config = BrainServicesConfiguration()
        services_config.load_config_section(yaml, brain_config, ".")

        self.assertFalse(services_config.exists("REST"))
        self.assertFalse(services_config.exists("Pannous"))
        self.assertFalse(services_config.exists("Pandora"))
        self.assertFalse(services_config.exists("Wikipedia"))
        self.assertFalse(services_config.exists("Other"))

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        services_config = BrainServicesConfiguration()
        services_config.load_config_section(yaml, brain_config, ".")

        self.assertFalse(services_config.exists("REST"))
        self.assertFalse(services_config.exists("Pannous"))
        self.assertFalse(services_config.exists("Pandora"))
        self.assertFalse(services_config.exists("Wikipedia"))
        self.assertFalse(services_config.exists("Other"))
