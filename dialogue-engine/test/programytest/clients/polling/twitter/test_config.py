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
from programy.clients.polling.twitter.config import TwitterConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class TwitterConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
            twitter:
              polling_interval: 59
              rate_limit_sleep: 900
              use_status: true
              use_direct_message: true
              auto_follow: true
              welcome_message: Thanks for following me
        """, ConsoleConfiguration(), ".")

        twitter_config = TwitterConfiguration()
        twitter_config.load_configuration(yaml, ".")

        self.assertEqual(59, twitter_config.polling_interval)
        self.assertEqual(900, twitter_config.rate_limit_sleep)
        self.assertTrue(twitter_config.use_status)
        self.assertTrue(twitter_config.use_direct_message)
        self.assertTrue(twitter_config.auto_follow)
        self.assertEqual("Thanks for following me", twitter_config.welcome_message)

    def test_to_yaml_with_defaults(self):
        config = TwitterConfiguration()

        data = {}
        config.to_yaml(data, True)

        self.assertEqual(data['polling_interval'], 0)
        self.assertEqual(data['rate_limit_sleep'], -1)
        self.assertEqual(data['use_status'], False)
        self.assertEqual(data['use_direct_message'], False)
        self.assertEqual(data['auto_follow'], False)
        self.assertEqual(data['welcome_message'], "Thanks for following me.")

        self.assertEqual(data['bot'], 'bot')
        self.assertEqual(data['bot_selector'], "programy.clients.client.DefaultBotSelector")
        self.assertEqual(data['renderer'], "programy.clients.render.text.TextRenderer")
