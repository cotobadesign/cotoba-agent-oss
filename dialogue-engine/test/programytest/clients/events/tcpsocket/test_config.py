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

from programy.clients.events.tcpsocket.config import SocketConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.events.console.config import ConsoleConfiguration


class SocketConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        socket:
          host: 127.0.0.1
          port: 9999
          queue: 5
          max_buffer: 1024
          debug: true
          """, ConsoleConfiguration(), ".")

        socket_config = SocketConfiguration()
        socket_config.load_configuration(yaml, ".")

        self.assertEqual("127.0.0.1", socket_config.host)
        self.assertEqual(9999, socket_config.port)
        self.assertEqual(5, socket_config.queue)
        self.assertEqual(1024, socket_config.max_buffer)
        self.assertEqual(True, socket_config.debug)

    def test_to_yaml_with_defaults(self):
        config = SocketConfiguration()

        data = {}
        config.to_yaml(data, True)

        self.assertEqual("0.0.0.0", data['host'])
        self.assertEqual(80, data['port'])
        self.assertEqual(5, data['queue'])
        self.assertEqual(1024, data['max_buffer'])
        self.assertEqual(False, data['debug'])

        self.assertEqual(data['bot'], 'bot')
        self.assertEqual(data['bot_selector'], "programy.clients.client.DefaultBotSelector")
        self.assertEqual(data['renderer'], "programy.clients.render.text.TextRenderer")

    def test_to_yaml_without_defaults(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        socket:
          host: 127.0.0.1
          port: 9999
          queue: 5
          max_buffer: 1024
          debug: true
          bot: bot
          default_userid: console
          prompt: $
          bot_selector: programy.clients.client.DefaultBotSelector
          renderer: programy.clients.render.text.TextRenderer
        """, ConsoleConfiguration(), ".")

        config = SocketConfiguration()
        config.load_configuration(yaml, ".")

        data = {}
        config.to_yaml(data, False)

        self.assertEqual("127.0.0.1", data['host'])
        self.assertEqual(9999, data['port'])
        self.assertEqual(5, data['queue'])
        self.assertEqual(1024, data['max_buffer'])
        self.assertEqual(True, data['debug'])

        self.assertEqual(data['bot'], 'bot')
        self.assertEqual(data['bot_selector'], "programy.clients.client.DefaultBotSelector")
        self.assertEqual(data['renderer'], "programy.clients.render.text.TextRenderer")
