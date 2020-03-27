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
from programy.translate.extension import TranslateExtension

from programytest.client import TestClient


class TranslateExtensionTests(unittest.TestCase):

    def setUp(self):
        self._client = TestClient()

        config = BotConfiguration()
        config._from_translator._classname = "programy.translate.textblob_translator.TextBlobTranslator"

        self.client_context = self._client.create_client_context("testuser")

        self.client_context._bot = Bot(config=config, client=self._client)
        self.client_context._bot.initiate_translator()

    def test_invalid_command(self):

        extension = TranslateExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(self.client_context, "XXX")
        self.assertIsNotNone(result)
        self.assertEqual("TRANSLATE INVALID COMMAND", result)

        result = extension.execute(self.client_context, "TRANSLATE")
        self.assertIsNotNone(result)
        self.assertEqual("TRANSLATE INVALID COMMAND", result)

        result = extension.execute(self.client_context, "TRANSLATE FROM")
        self.assertIsNotNone(result)
        self.assertEqual("TRANSLATE INVALID COMMAND", result)

        result = extension.execute(self.client_context, "TRANSLATE FROM EN")
        self.assertIsNotNone(result)
        self.assertEqual("TRANSLATE INVALID COMMAND", result)

        result = extension.execute(self.client_context, "TRANSLATE FROM EN TO")
        self.assertIsNotNone(result)
        self.assertEqual("TRANSLATE INVALID COMMAND", result)

        result = extension.execute(self.client_context, "TRANSLATE FROM EN TO FR")
        self.assertIsNotNone(result)
        self.assertEqual("TRANSLATE INVALID COMMAND", result)

    def test_valid_scores_command(self):

        extension = TranslateExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(self.client_context, "TRANSLATE ENABLED")
        self.assertIsNotNone(result)
        self.assertEqual("TRANSLATE ENABLED", result)

        result = extension.execute(self.client_context, "TRANSLATE FROM EN TO FR HELLO I LOVE YOU")
        self.assertIsNotNone(result)
        self.assertEqual("TRANSLATED SALUT JE T'AIME", result)
