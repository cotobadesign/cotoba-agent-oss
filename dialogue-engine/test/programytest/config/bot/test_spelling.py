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
from programy.config.bot.spelling import BotSpellingConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class BotSpellingConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            spelling:
              classname: programy.spelling.norvig.NorvigSpellingChecker
              alphabet: abcdefghijklmnopqrstuvwxyz
              check_before: true
              check_and_retry: true
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        spelling_config = BotSpellingConfiguration()
        spelling_config.load_config_section(yaml, bot_config, ".")

        self.assertEqual("programy.spelling.norvig.NorvigSpellingChecker", spelling_config.classname)
        self.assertEqual("abcdefghijklmnopqrstuvwxyz", spelling_config.alphabet)
        self.assertTrue(spelling_config.check_before)
        self.assertTrue(spelling_config.check_and_retry)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            spelling:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        spelling_config = BotSpellingConfiguration()
        spelling_config.load_config_section(yaml, bot_config, ".")

        self.assertIsNone(spelling_config.classname)
        self.assertIsNone(spelling_config.alphabet)
        self.assertFalse(spelling_config.check_before)
        self.assertFalse(spelling_config.check_and_retry)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        spelling_config = BotSpellingConfiguration()
        spelling_config.load_config_section(yaml, bot_config, ".")

        self.assertIsNone(spelling_config.classname)
        self.assertIsNone(spelling_config.alphabet)
        self.assertFalse(spelling_config.check_before)
        self.assertFalse(spelling_config.check_and_retry)
