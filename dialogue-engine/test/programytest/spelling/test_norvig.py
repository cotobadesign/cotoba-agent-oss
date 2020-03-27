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
from programy.spelling.norvig import NorvigSpellingChecker
from programy.config.bot.spelling import BotSpellingConfiguration

from programytest.client import TestClient


class NorvigSpellingCheckerTests(unittest.TestCase):

    def test_spellchecker(self):
        client = TestClient()

        client.add_license_keys_store()
        client.add_spelling_store()

        checker = NorvigSpellingChecker()
        self.assertIsNotNone(checker)
        checker.initialise(client.storage_factory)

        self.assertEqual("THIS", checker.correct("THIS"))
        self.assertEqual("THIS", checker.correct("This"))
        self.assertEqual("THIS", checker.correct("this"))

        self.assertEqual("LOCATION", checker.correct("LOCETION"))
        self.assertEqual("LOCATION", checker.correct("Locetion"))
        self.assertEqual("LOCATION", checker.correct("locetion"))

    def test_initiate_spellchecker(self):

        spelling_config = BotSpellingConfiguration()
        spelling_config._load = True
        spelling_config._classname = "programy.spelling.norvig.NorvigSpellingChecker"

        client = TestClient()
        storage_factory = client.storage_factory

        spell_checker = SpellingChecker.initiate_spellchecker(spelling_config, storage_factory)

        self.assertIsNotNone(spell_checker)
