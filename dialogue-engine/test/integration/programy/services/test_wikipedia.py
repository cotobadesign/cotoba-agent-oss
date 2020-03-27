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
import os

from programy.utils.license.keys import LicenseKeys
from programy.services.wikipediaservice import WikipediaService


class TestBot:

    def __init__(self):
        self.license_keys = None


class WikipediaServiceTests(unittest.TestCase):

    def setUp(self):
        self.bot = TestBot()
        self.bot.license_keys = LicenseKeys()
        self.bot.license_keys.load_license_key_file(os.path.dirname(__file__) + os.sep + "test.keys")

    def test_ask_question_summary(self):
        service = WikipediaService()
        self.assertIsNotNone(service)

        response = service.ask_question(self.bot, "SUMMARY cat")
        self.assertIsNotNone(response)
        self.assertEqual("The domestic cat (Felis silvestris catus or Felis catus) is a small, typically furry, carnivorous mammal.", response)

    def test_ask_question_search(self):
        service = WikipediaService()
        self.assertIsNotNone(service)

        response = service.ask_question(self.bot, "SEARCH cat")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("Cat"))
