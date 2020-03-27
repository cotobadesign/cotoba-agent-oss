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
from programy.utils.email.config import EmailConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class EmailConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
            email:
                host: 127.0.0.1
                port: 80
                username: emailuser
                password: emailpassword
                from_addr: emailfromuser
        """, ConsoleConfiguration(), ".")

        client_config = yaml.get_section("console")

        email_config = EmailConfiguration()
        email_config.load_config_section(yaml, client_config, ".")

        self.assertEqual("127.0.0.1", email_config.host)
        self.assertEqual(80, email_config.port)
        self.assertEqual("emailuser", email_config.username)
        self.assertEqual("emailpassword", email_config.password)
        self.assertEqual("emailfromuser", email_config.from_addr)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
            email:
        """, ConsoleConfiguration(), ".")

        client_config = yaml.get_section("email")

        email_config = EmailConfiguration()
        email_config.load_config_section(yaml, client_config, ".")

        self.assertIsNone(email_config.host)
        self.assertIsNone(email_config.port)
        self.assertIsNone(email_config.username)
        self.assertIsNone(email_config.password)
        self.assertIsNone(email_config.from_addr)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
        """, ConsoleConfiguration(), ".")

        client_config = yaml.get_section("email")

        email_config = EmailConfiguration()
        email_config.load_config_section(yaml, client_config, ".")

        self.assertIsNone(email_config.host)
        self.assertIsNone(email_config.port)
        self.assertIsNone(email_config.username)
        self.assertIsNone(email_config.password)
        self.assertIsNone(email_config.from_addr)
