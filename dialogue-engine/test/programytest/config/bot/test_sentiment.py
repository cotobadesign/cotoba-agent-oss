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
from programy.config.bot.sentiment import BotSentimentAnalyserConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class BotSentimentAnalyserConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            sentiment:
                classname: programy.sentiment.textblob_sentiment.TextBlobSentimentAnalyser
                scores: programy.sentiment.scores.SentimentScores
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        sentiment_config = BotSentimentAnalyserConfiguration()
        sentiment_config.load_config_section(yaml, bot_config, ".")

        self.assertEqual("programy.sentiment.textblob_sentiment.TextBlobSentimentAnalyser", sentiment_config.classname)
        self.assertEqual("programy.sentiment.scores.SentimentScores", sentiment_config.scores)

    def test_with_default_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            sentiment:
                classname: programy.sentiment.textblob_sentiment.TextBlobSentimentAnalyser
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        sentiment_config = BotSentimentAnalyserConfiguration()
        sentiment_config.load_config_section(yaml, bot_config, ".")

        self.assertEqual("programy.sentiment.textblob_sentiment.TextBlobSentimentAnalyser", sentiment_config.classname)
        self.assertEqual("programy.sentiment.scores.SentimentScores", sentiment_config.scores)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            sentiment:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        sentiment_config = BotSentimentAnalyserConfiguration()
        sentiment_config.load_config_section(yaml, bot_config, ".")

        self.assertIsNone(sentiment_config.classname)
        self.assertIsNone(sentiment_config.scores)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        sentiment_config = BotSentimentAnalyserConfiguration()
        sentiment_config.load_config_section(yaml, bot_config, ".")

        self.assertIsNone(sentiment_config.classname)
        self.assertIsNone(sentiment_config.scores)
