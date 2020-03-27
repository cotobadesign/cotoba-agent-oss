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
from programy.clients.polling.telegram.config import TelegramConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class TelegramClientConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
            telegram:
              unknown_command: Sorry, that is not a command I have been taught yet!
              unknown_command_srai: YTELEGRAM_UNKNOWN_COMMAND
          """, ConsoleConfiguration(), ".")

        telegram_config = TelegramConfiguration()
        telegram_config.load_configuration(yaml, ".")

        self.assertEqual(telegram_config.unknown_command, "Sorry, that is not a command I have been taught yet!")
        self.assertEqual(telegram_config.unknown_command_srai, "YTELEGRAM_UNKNOWN_COMMAND")

    def test_to_yaml_with_defaults(self):
        config = TelegramConfiguration()

        data = {}
        config.to_yaml(data, True)

        self.assertEqual('Sorry, that is not a command I have been taught yet!', data['unknown_command'])
        self.assertEqual('YTELEGRAM_UNKNOWN_COMMAND', data['unknown_command_srai'])

        self.assertEqual(data['bot'], 'bot')
        self.assertEqual(data['bot_selector'], "programy.clients.client.DefaultBotSelector")
        self.assertEqual(data['renderer'], "programy.clients.render.text.TextRenderer")
