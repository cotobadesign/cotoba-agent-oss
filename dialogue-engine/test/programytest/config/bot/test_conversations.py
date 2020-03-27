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

from programy.config.bot.conversations import BotConversationsConfiguration
from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


class BotConversationsConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            conversations:
              max_histories: 666
              initial_topic: topic1
              restore_last_topic: true
              multi_client: true

        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        convo_config = BotConversationsConfiguration()
        convo_config.load_config_section(yaml, bot_config, ".")

        self.assertEqual(convo_config.section_name, "conversations")

        self.assertEqual(666, convo_config.max_histories)
        self.assertEqual("topic1", convo_config.initial_topic)
        self.assertTrue(convo_config.restore_last_topic)
        self.assertTrue(convo_config.multi_client)

    def test_with_defaults(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            conversations:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        convo_config = BotConversationsConfiguration()
        convo_config.load_config_section(yaml, bot_config, ".")

        self.assertEqual(convo_config.section_name, "conversations")

        self.assertEqual(100, convo_config.max_histories)
        self.assertEqual("*", convo_config.initial_topic)
        self.assertFalse(convo_config.restore_last_topic)
        self.assertFalse(convo_config.multi_client)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        convo_config = BotConversationsConfiguration()
        convo_config.load_config_section(yaml, bot_config, ".")

        self.assertEqual(convo_config.section_name, "conversations")

        self.assertEqual(100, convo_config.max_histories)
        self.assertEqual("*", convo_config.initial_topic)
        self.assertFalse(convo_config.restore_last_topic)
        self.assertFalse(convo_config.multi_client)
