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
import re
from programy.processors.post.denormalize import DenormalizePostProcessor
from programy.processors.post.formatpunctuation import FormatPunctuationProcessor
from programy.processors.post.formatnumbers import FormatNumbersPostProcessor
from programy.processors.post.multispaces import RemoveMultiSpacePostProcessor
from programy.processors.post.emojize import EmojizePostProcessor
from programy.processors.post.translate import TranslatorPostProcessor
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext

from programytest.client import TestClient


class PostProcessingTests(unittest.TestCase):

    def post_process(self, output_str):
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
        context.bot.brain.denormals.add_to_lookup("dot com", '.com ')
        context.bot.brain.denormals.add_to_lookup("atsign", '@')

        denormalize = DenormalizePostProcessor()
        punctuation = FormatPunctuationProcessor()
        numbers = FormatNumbersPostProcessor()
        multispaces = RemoveMultiSpacePostProcessor()
        emojize = EmojizePostProcessor()
        translate = TranslatorPostProcessor()

        output_str = denormalize.process(context, output_str)
        output_str = punctuation.process(context, output_str)
        output_str = numbers.process(context, output_str)
        output_str = multispaces.process(context, output_str)
        output_str = emojize.process(context, output_str)
        output_str = translate.process(context, output_str)

        return output_str

    def test_post_cleanup(self):

        result = self.post_process("Hello World")
        self.assertIsNotNone(result)
        self.assertEqual("Bonjour le monde", result)

        result = self.post_process("Hello World . This is It! ")
        self.assertIsNotNone(result)
        self.assertEqual("Bonjour le monde. Ça y est!", result)

        result = self.post_process("My email address is ybot atsign programy dot com")
        self.assertIsNotNone(result)
        self.assertEqual("Mon adresse e-mail est ybot@programy.com", result)

        result = self.post_process("He said ' Hello World '.")
        self.assertIsNotNone(result)
        self.assertEqual('Il a dit "Bonjour tout le monde".', result)
