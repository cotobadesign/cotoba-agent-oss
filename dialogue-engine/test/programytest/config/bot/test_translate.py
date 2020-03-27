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
from programy.config.bot.translation import BotTranslatorConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class BotTranslatorConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            translator:
                classname: programy.translate.textblob_translator.TextBlobTranslator
                from: fr
                to: en
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        translator_config = BotTranslatorConfiguration(name="translator")
        translator_config.load_config_section(yaml, bot_config, ".")

        self.assertEqual("programy.translate.textblob_translator.TextBlobTranslator", translator_config.classname)
        self.assertEqual("en", translator_config.to_lang)
        self.assertEqual("fr", translator_config.from_lang)

    def test_with_default_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            translator:
                classname: programy.translate.textblob_translator.TextBlobTranslator
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        translator_config = BotTranslatorConfiguration(name="translator")
        translator_config.load_config_section(yaml, bot_config, ".")

        self.assertEqual("programy.translate.textblob_translator.TextBlobTranslator", translator_config.classname)
        self.assertIsNone(translator_config.to_lang)
        self.assertIsNone(translator_config.from_lang)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            translator:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        translator_config = BotTranslatorConfiguration(name="translator")
        translator_config.load_config_section(yaml, bot_config, ".")

        self.assertIsNone(translator_config.classname)
        self.assertIsNone(translator_config.from_lang)
        self.assertIsNone(translator_config.to_lang)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        translator_config = BotTranslatorConfiguration(name="translator")
        translator_config.load_config_section(yaml, bot_config, ".")

        self.assertIsNone(translator_config.classname)
        self.assertIsNone(translator_config.from_lang)
        self.assertIsNone(translator_config.to_lang)
