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

from programy.dialog.tokenizer.tokenizer import Tokenizer
from programy.config.brain.brain import BrainConfiguration
from programy.config.brain.tokenizer import BrainTokenizerConfiguration


class TokenizerTests(unittest.TestCase):

    def test_default_tokenizer(self):
        tokenizer = Tokenizer()
        self.assertIsNotNone(tokenizer)

        self.assertEqual([], tokenizer.texts_to_words(""))
        self.assertEqual(["Hello"], tokenizer.texts_to_words("Hello"))
        self.assertEqual(["Hello", "World"], tokenizer.texts_to_words("Hello World"))
        self.assertEqual(["Hello", "World"], tokenizer.texts_to_words(" Hello   World "))

        self.assertEqual("", tokenizer.words_to_texts([]))
        self.assertEqual("Hello", tokenizer.words_to_texts(["Hello"]))
        self.assertEqual("Hello World", tokenizer.words_to_texts(["Hello", "World"]))
        self.assertEqual("Hello World", tokenizer.words_to_texts(["Hello", "", "World"]))
        self.assertEqual("Hello World", tokenizer.words_to_texts([" Hello ", " World "]))

    def test_load_tokenizer(self):

        config = BrainConfiguration()
        self.assertIsNotNone(config)
        tokenizer_config = BrainTokenizerConfiguration()
        self.assertIsNotNone(tokenizer_config)
        tokenizer_config._classname = 'programy.dialog.tokenizer.tokenizer.Tokenizer'
        tokenizer_config._punctation_chars = ''
        config._tokenizer = tokenizer_config

        tokenizer = Tokenizer.load_tokenizer(config)
        self.assertIsNotNone(tokenizer)
        self.assertIsInstance(tokenizer, Tokenizer)

    def test_load_tokenizer_no_class(self):

        config = BrainConfiguration()
        self.assertIsNotNone(config)
        tokenizer_config = BrainTokenizerConfiguration()
        self.assertIsNotNone(tokenizer_config)
        tokenizer_config._classname = None
        tokenizer_config._punctation_chars = ''
        config._tokenizer = tokenizer_config

        tokenizer = Tokenizer.load_tokenizer(config)
        self.assertIsNotNone(tokenizer)
        self.assertIsInstance(tokenizer, Tokenizer)

    def test_tokenizer_is_template(self):
        tokenizer = Tokenizer()
        self.assertIsNotNone(tokenizer)

        self.assertFalse(tokenizer.is_template)

        tokenizer.is_template = True
        self.assertTrue(tokenizer.is_template)

    def test_tokenizer_words_from_current_pos(self):
        tokenizer = Tokenizer()
        self.assertIsNotNone(tokenizer)

        self.assertEqual("", tokenizer.words_from_current_pos(None, 0))

        words = ["aaa", "bbb", "ccc"]
        self.assertEqual("aaa bbb ccc", tokenizer.words_from_current_pos(words, 0))
        self.assertEqual("bbb ccc", tokenizer.words_from_current_pos(words, 1))
        self.assertEqual("ccc", tokenizer.words_from_current_pos(words, 2))
        self.assertEqual("", tokenizer.words_from_current_pos(words, 3))
        self.assertEqual("ccc", tokenizer.words_from_current_pos(words, -1))
        self.assertEqual("bbb ccc", tokenizer.words_from_current_pos(words, -2))
        self.assertEqual("aaa bbb ccc", tokenizer.words_from_current_pos(words, -3))
        self.assertEqual("aaa bbb ccc", tokenizer.words_from_current_pos(words, -4))

    def test_tokenizer_compare(self):
        tokenizer = Tokenizer()
        self.assertIsNotNone(tokenizer)

        target = "aaa bbb"
        self.assertTrue(tokenizer.compare(target, "aaa bbb"))
        self.assertFalse(tokenizer.compare(target, "aaa"))
        self.assertFalse(tokenizer.compare(target, "bbb"))
