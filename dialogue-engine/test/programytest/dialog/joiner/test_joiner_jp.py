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

from programy.dialog.joiner.joiner_jp import SentenceJoiner
from programy.config.bot.joiner import BotSentenceJoinerConfiguration


class SentenceJoinerJPTests(unittest.TestCase):

    def test_initiate_joiner(self):

        config = BotSentenceJoinerConfiguration()
        self.assertIsNotNone(config)
        config._classname = 'programy.dialog.joiner.joiner_jp.SentenceJoiner'
        config._join_chars = '.?!。？！'
        config._terminator = '。'

        joiner = SentenceJoiner.initiate_sentence_joiner(config)
        self.assertIsNotNone(joiner)
        self.assertIsInstance(joiner, SentenceJoiner)

    def test_initiate_class_none(self):

        config = BotSentenceJoinerConfiguration()
        self.assertIsNotNone(config)
        config._classname = None
        config._join_chars = '.?!。？！'
        config._terminator = '。'

        joiner = SentenceJoiner.initiate_sentence_joiner(config)
        self.assertIsNone(joiner)

    def test_combine_answers(self):

        config = BotSentenceJoinerConfiguration()
        self.assertIsNotNone(config)
        config._classname = 'programy.dialog.joiner.joiner_jp.SentenceJoiner'
        config._join_chars = '.?!。？！'
        config._terminator = '。'

        joiner = SentenceJoiner.initiate_sentence_joiner(config)
        self.assertIsNotNone(joiner)

        self.assertEquals("", joiner.combine_answers([""], False))

        self.assertEquals("this is a pen。", joiner.combine_answers(["this is a pen"], False))
        self.assertEquals("こんにちは。", joiner.combine_answers(["こんにちは"], False))
        self.assertEquals("this is a pen.", joiner.combine_answers(["this is a pen."], False))
        self.assertEquals("こんにちは。", joiner.combine_answers(["こんにちは。"], False))
        self.assertEquals("is this a pen?", joiner.combine_answers(["is this a pen?"], False))
        self.assertEquals("こんにちは？", joiner.combine_answers(["こんにちは？"], False))
        self.assertEquals("is this a pen!", joiner.combine_answers(["is this a pen!"], False))
        self.assertEquals("こんにちは！", joiner.combine_answers(["こんにちは！"], False))

    def test_combine_answers_srai(self):

        config = BotSentenceJoinerConfiguration()
        self.assertIsNotNone(config)
        config._classname = 'programy.dialog.joiner.joiner_jp.SentenceJoiner'
        config._join_chars = '.?!。？！'
        config._terminator = '。'

        joiner = SentenceJoiner.initiate_sentence_joiner(config)
        self.assertIsNotNone(joiner)

        self.assertEquals("this is a pen", joiner.combine_answers(["this is a pen"], True))
        self.assertEquals("こんにちは", joiner.combine_answers(["こんにちは"], True))
        self.assertEquals("this is a pen.", joiner.combine_answers(["this is a pen."], True))
        self.assertEquals("こんにちは。", joiner.combine_answers(["こんにちは。"], True))
        self.assertEquals("is this a pen?", joiner.combine_answers(["is this a pen?"], True))
        self.assertEquals("こんにちは？", joiner.combine_answers(["こんにちは？"], True))
        self.assertEquals("is this a pen!", joiner.combine_answers(["is this a pen!"], True))
        self.assertEquals("こんにちは！", joiner.combine_answers(["こんにちは！"], True))
