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
from programy.config.brain.service import BrainServiceConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class BrainServiceConfigurationTests(unittest.TestCase):

    def test_rest_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            services:
                REST:
                    classname: programy.services.rest.GenericRESTService
                    method: GET
                    host: 0.0.0.0
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        services_config = yaml.get_section("services", brain_config)
        self.assertIsNotNone(services_config)

        service_config = BrainServiceConfiguration("REST")
        service_config.load_config_section(yaml, services_config, ".")

        self.assertEqual("programy.services.rest.GenericRESTService", service_config.classname)
        self.assertEqual("GET", service_config.method)
        self.assertEqual("0.0.0.0", service_config.host)
        self.assertIsNone(service_config.port)
        self.assertIsNone(service_config.url)

    def test_pannous_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            services:
                Pannous:
                    classname: programy.services.pannous.PannousService
                    url: http://weannie.pannous.com/api
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        services_config = yaml.get_section("services", brain_config)
        self.assertIsNotNone(services_config)

        service_config = BrainServiceConfiguration("Pannous")
        service_config.load_config_section(yaml, services_config, ".")

        self.assertEqual("programy.services.pannous.PannousService", service_config.classname)
        self.assertEqual("http://weannie.pannous.com/api", service_config.url)
        self.assertIsNone(service_config.method)
        self.assertIsNone(service_config.host)
        self.assertIsNone(service_config.port)

    def test_pandora_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            services:
                Pandora:
                    classname: programy.services.pandora.PandoraService
                    url: http://www.pandorabots.com/pandora/talk-xml
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        services_config = yaml.get_section("services", brain_config)
        self.assertIsNotNone(services_config)

        service_config = BrainServiceConfiguration("Pandora")
        service_config.load_config_section(yaml, services_config, ".")

        self.assertEqual("programy.services.pandora.PandoraService", service_config.classname)
        self.assertEqual("http://www.pandorabots.com/pandora/talk-xml", service_config.url)
        self.assertIsNone(service_config.method)
        self.assertIsNone(service_config.host)
        self.assertIsNone(service_config.port)

    def test_wikipedia_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            services:
                Wikipedia:
                    classname: programy.services.wikipediaservice.WikipediaService
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        services_config = yaml.get_section("services", brain_config)
        self.assertIsNotNone(services_config)

        service_config = BrainServiceConfiguration("Wikipedia")
        service_config.load_config_section(yaml, services_config, ".")

        self.assertEqual("programy.services.wikipediaservice.WikipediaService", service_config.classname)
        self.assertIsNone(service_config.method)
        self.assertIsNone(service_config.host)
        self.assertIsNone(service_config.port)
        self.assertIsNone(service_config.url)

    def test_rest_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            services:
                REST:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        services_config = yaml.get_section("services", brain_config)
        self.assertIsNotNone(services_config)

        service_config = BrainServiceConfiguration("REST")
        service_config.load_config_section(yaml, services_config, ".")

        self.assertIsNone(service_config.classname)
        self.assertIsNone(service_config.method)
        self.assertIsNone(service_config.host)
        self.assertIsNone(service_config.port)
        self.assertIsNone(service_config.url)
