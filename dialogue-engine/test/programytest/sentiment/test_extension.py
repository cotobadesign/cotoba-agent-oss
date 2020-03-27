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

from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.sentiment.extension import SentimentExtension

from programytest.client import TestClient


class SentimentExtensionTests(unittest.TestCase):

    def setUp(self):
        self._client = TestClient()

        config = BotConfiguration()
        config.sentiment_analyser._classname = "programy.sentiment.textblob_sentiment.TextBlobSentimentAnalyser"
        config.sentiment_analyser._scores = "programy.sentiment.scores.SentimentScores"

        self.client_context = self._client.create_client_context("testuser")

        self.client_context._bot = Bot(config=config, client=self._client)
        self.client_context._bot.initiate_sentiment_analyser()

    def test_invalid_command(self):

        extension = SentimentExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(self.client_context, "XXX")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT INVALID COMMAND", result)

        result = extension.execute(self.client_context, "SENTIMENT")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT INVALID COMMAND", result)

        result = extension.execute(self.client_context, "SENTIMENT SCOREX")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT INVALID COMMAND", result)

        result = extension.execute(self.client_context, "SENTIMENT FEELING")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT INVALID COMMAND", result)

        result = extension.execute(self.client_context, "SENTIMENT FEELING LAST")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT INVALID COMMAND", result)

        result = extension.execute(self.client_context, "SENTIMENT SCORES")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT INVALID COMMAND", result)

        result = extension.execute(self.client_context, "SENTIMENT CURRENT")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT INVALID COMMAND", result)

    def test_valid_scores_command(self):

        extension = SentimentExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(self.client_context, "SENTIMENT ENABLED")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT ENABLED", result)

        result = extension.execute(self.client_context, "SENTIMENT FEELING LAST 1")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT FEELING NEUTRAL AND NEUTRAL", result)

        result = extension.execute(self.client_context, "SENTIMENT FEELING OVERALL")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT FEELING NEUTRAL AND NEUTRAL", result)

        result = extension.execute(self.client_context, "SENTIMENT SCORE I LIKE YOU")
        self.assertIsNotNone(result)
        self.assertEqual("SENTIMENT SCORES POSITIVITY NEUTRAL SUBJECTIVITY COMPLETELY OBJECTIVE", result)
