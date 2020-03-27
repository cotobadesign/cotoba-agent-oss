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
from programy.spelling.extension import SpellingExtension
from programy.spelling.norvig import NorvigSpellingChecker

from programytest.client import TestClient


class NorvigSpellingExtensionTests(unittest.TestCase):

    def setUp(self):
        self._client = TestClient()

        config = BotConfiguration()

        self.client_context = self._client.create_client_context("testuser")

        self.client_context._bot = Bot(config=config, client=self._client)
        self.client_context._bot._spell_checker = NorvigSpellingChecker()
        self.client_context._bot._spell_checker.add_corpus("THIS IS HAVE WORDS SPELLED CORRECTLY")

    def test_invalid_command(self):

        extension = SpellingExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(self.client_context, "XXX")
        self.assertIsNotNone(result)
        self.assertEqual("SPELLING CORRECT INVALID COMMAND", result)

        result = extension.execute(self.client_context, "SPELLING")
        self.assertIsNotNone(result)
        self.assertEqual("SPELLING CORRECT INVALID COMMAND", result)

        result = extension.execute(self.client_context, "SPELLING CORRECT")
        self.assertIsNotNone(result)
        self.assertEqual("SPELLING CORRECT INVALID COMMAND", result)

    def test_valid_scores_command(self):

        extension = SpellingExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(self.client_context, "SPELLING ENABLED")
        self.assertIsNotNone(result)
        self.assertEqual("SPELLING ENABLED", result)

        result = extension.execute(self.client_context, "SPELLING CORRECT HAVVE")
        self.assertIsNotNone(result)
        self.assertEqual("SPELLING CORRECTED HAVE", result)
