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
from programy.processors.post.translate import TranslatorPostProcessor
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration

from programytest.client import TestClient


class MockClientContext(object):

    def __init__(self, bot):
        self.bot = bot


class TranslatorPostProcessorTest(unittest.TestCase):

    def setUp(self):
        self.client = TestClient()
        config = BotConfiguration()

        config.from_translator._classname = "programy.translate.textblob_translator.TextBlobTranslator"
        config.from_translator._from_lang = "fr"
        config.from_translator._to_lang = "en"

        config.to_translator._classname = "programy.translate.textblob_translator.TextBlobTranslator"
        config.to_translator._from_lang = "en"
        config.to_translator._to_lang = "fr"

        self.bot = Bot(config=config, client=self.client)
        self.bot.initiate_translator()

    def test_post_process_translate(self):
        processor = TranslatorPostProcessor()

        context = MockClientContext(self.bot)

        self.assertEqual("Bonjour", processor.process(context, "Hello"))
