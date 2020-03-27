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
from programy.triggers.config import TriggerConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class TriggersConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
            triggers:
                manager: programy.triggers.rest.RestTriggerManager
        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")

        triggers_config = TriggerConfiguration()
        triggers_config.load_config_section(yaml, console_config, ".")

        self.assertEquals("programy.triggers.rest.RestTriggerManager", triggers_config.manager)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            triggers:
        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")

        triggers_config = TriggerConfiguration()
        triggers_config.load_config_section(yaml, console_config, ".")

        self.assertEquals("programy.triggers.local.LocalTriggerManager", triggers_config.manager)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")

        triggers_config = TriggerConfiguration()
        triggers_config.load_config_section(yaml, console_config, ".")

        self.assertEquals("programy.triggers.local.LocalTriggerManager", triggers_config.manager)

    def test_with_additional_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
            triggers:
                manager: programy.triggers.rest.RestTriggerManager
                url: http://localhost:8989/api/v1.0/trigger
                method: POST
                token: 123BC4F3D
        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")

        triggers_config = TriggerConfiguration()
        triggers_config.load_config_section(yaml, console_config, ".")

        self.assertEquals("programy.triggers.rest.RestTriggerManager", triggers_config.manager)
        self.assertEquals(triggers_config.value("url"), "http://localhost:8989/api/v1.0/trigger")
        self.assertEquals(triggers_config.value("method"), "POST")
        self.assertEquals(triggers_config.value("token"), "123BC4F3D")
