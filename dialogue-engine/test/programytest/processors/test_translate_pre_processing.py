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
from programy.processors.pre.removepunctuation import RemovePunctuationPreProcessor
from programy.processors.pre.toupper import ToUpperPreProcessor
from programy.processors.pre.normalize import NormalizePreProcessor
from programy.processors.pre.demojize import DemojizePreProcessor
from programy.processors.pre.translate import TranslatorPreProcessor
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext

from programytest.client import TestClient


class PreProcessingTests(unittest.TestCase):

    def test_pre_cleanup(self):
        self.client = TestClient()

        context = ClientContext(self.client, "testid")

        config = BotConfiguration()

        config.from_translator._classname = "programy.translate.textblob_translator.TextBlobTranslator"
        config.from_translator._from_lang = "fr"
        config.from_translator._to_lang = "en"

        config.to_translator._classname = "programy.translate.textblob_translator.TextBlobTranslator"
        config.to_translator._from_lang = "en"
        config.to_translator._to_lang = "fr"

        context.bot = Bot(config=config, client=self.client)
        context.brain = context.bot.brain
        test_str = "Ceci est mon emplacement!"

        translate_processor = TranslatorPreProcessor()
        test_str = translate_processor.process(context, test_str)
        self.assertEqual("This is my location!", test_str)

        punctuation_processor = RemovePunctuationPreProcessor()
        test_str = punctuation_processor.process(context, test_str)
        self.assertEqual("This is my location!", test_str)

        normalize_processor = NormalizePreProcessor()
        test_str = normalize_processor.process(context, test_str)
        self.assertEqual("This is my location!", test_str)

        toupper_processor = ToUpperPreProcessor()
        test_str = toupper_processor.process(context, test_str)
        self.assertEqual("THIS IS MY LOCATION!", test_str)

        demojize_processpr = DemojizePreProcessor()
        test_str = demojize_processpr.process(context, test_str)
        self.assertEqual(test_str, test_str)
