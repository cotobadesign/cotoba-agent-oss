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

from programy.spelling.base import SpellingChecker
from programy.config.bot.spelling import BotSpellingConfiguration
from programy.dialog.sentence import Sentence

from programytest.client import TestClient


class MockSpellingChecker(SpellingChecker):

    def __init__(self, spelling_config=None):
        SpellingChecker.__init__(self, spelling_config)

    def correct(self, phrase):
        return "Hello World"


class MockBrain(object):

    def __init__(self):
        self.id = 'id'

    def ask_question(self, client_context, each_sentence):
        return "Hello World"


class SpellingCheckerTests(unittest.TestCase):

    def test_ensure_not_implemented(self):

        checker = SpellingChecker()
        self.assertIsNotNone(checker)
        with self.assertRaises(Exception):
            checker.correct("Test This")

    def test_initiate_spellchecker(self):

        spelling_config = BotSpellingConfiguration()
        spelling_config._classname = "programytest.spelling.test_base.MockSpellingChecker"

        storage_factory = None

        spell_checker = SpellingChecker.initiate_spellchecker(spelling_config, storage_factory)

        self.assertIsNotNone(spell_checker)

    def test_initiate_spellchecker_no_classname(self):

        spelling_config = BotSpellingConfiguration()
        spelling_config._classname = None

        storage_factory = None

        spell_checker = SpellingChecker.initiate_spellchecker(spelling_config, storage_factory)

        self.assertIsNone(spell_checker)

    def test_initiate_spellchecker_invalid_classname(self):

        spelling_config = BotSpellingConfiguration()
        spelling_config._classname = "programytest.spelling.test_base.InvalidSpellingChecker"

        storage_factory = None

        spell_checker = SpellingChecker.initiate_spellchecker(spelling_config, storage_factory)

        self.assertIsNone(spell_checker)

    def test_check_spelling_before_true(self):
        spelling_config = BotSpellingConfiguration()
        spelling_config._classname = "programytest.spelling.test_base.MockSpellingChecker"
        spelling_config._check_before = True

        storage_factory = None

        spell_checker = SpellingChecker.initiate_spellchecker(spelling_config, storage_factory)

        client = TestClient()
        client_context = client.create_client_context("user1")

        sentence = Sentence(client_context.brain.tokenizer, "Hello word")

        spell_checker.check_spelling_before(client_context, sentence)

        self.assertEqual(sentence.text(), "Hello World")

    def test_check_spelling_before_false(self):
        spelling_config = BotSpellingConfiguration()
        spelling_config._classname = "programytest.spelling.test_base.MockSpellingChecker"
        spelling_config._check_before = False

        storage_factory = None

        spell_checker = SpellingChecker.initiate_spellchecker(spelling_config, storage_factory)

        client = TestClient()
        client_context = client.create_client_context("user1")

        sentence = Sentence(client_context.brain.tokenizer, "Hello word")

        spell_checker.check_spelling_before(client_context, sentence)

        self.assertEqual(sentence.text(), "Hello word")

    def test_check_spelling_and_retry_true(self):
        spelling_config = BotSpellingConfiguration()
        spelling_config._classname = "programytest.spelling.test_base.MockSpellingChecker"
        spelling_config._check_and_retry = True

        storage_factory = None

        spell_checker = SpellingChecker.initiate_spellchecker(spelling_config, storage_factory)

        client = TestClient()
        client_context = client.create_client_context("user1")
        tokenizer = client_context.brain.tokenizer
        client_context._brain = MockBrain()

        sentence = Sentence(tokenizer, "Hello word")

        response = spell_checker.check_spelling_and_retry(client_context, sentence)

        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello World")

    def test_check_spelling_and_retry_false(self):
        spelling_config = BotSpellingConfiguration()
        spelling_config._classname = "programytest.spelling.test_base.MockSpellingChecker"
        spelling_config._check_and_retry = False

        storage_factory = None

        spell_checker = SpellingChecker.initiate_spellchecker(spelling_config, storage_factory)

        client = TestClient()
        client_context = client.create_client_context("user1")
        tokenizer = client_context.brain.tokenizer
        client_context._brain = MockBrain()

        sentence = Sentence(tokenizer, "Hello word")

        response = spell_checker.check_spelling_and_retry(client_context, sentence)

        self.assertIsNone(response)
