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

from programytest.client import TestClient


class SpaceTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(SpaceTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class SpaceAIMLTests(unittest.TestCase):

    def setUp(self):
        client = SpaceTestClient()
        self._client_context = client.create_client_context("testid")

    def test_space_only(self):
        response = self._client_context.bot.ask_question(self._client_context, "SPACE only")
        self.assertEqual(response, "")

    def test_en_front_space(self):
        response = self._client_context.bot.ask_question(self._client_context, "en front SPACE")
        self.assertEqual(response, 'Test.')

    def test_en_middle_space(self):
        response = self._client_context.bot.ask_question(self._client_context, "en middle SPACE")
        self.assertEqual(response, "Test data.")

    def test_en_last_space(self):
        response = self._client_context.bot.ask_question(self._client_context, "en last SPACE")
        self.assertEqual(response, 'Test.')

    def test_en_space_before_tag(self):
        response = self._client_context.bot.ask_question(self._client_context, "en SPACE before TAG")
        self.assertEqual(response, 'Test.')

    def test_en_space_between_tag(self):
        response = self._client_context.bot.ask_question(self._client_context, "en no SPACE between TAG")
        self.assertEqual(response, "Test data.")

        response = self._client_context.bot.ask_question(self._client_context, "en SPACE between TAG")
        self.assertEqual(response, "Test data.")

    def test_en_space_after_tag(self):
        response = self._client_context.bot.ask_question(self._client_context, "en SPACE after TAG")
        self.assertEqual(response, 'Test.')

    def test_jp_front_space(self):
        response = self._client_context.bot.ask_question(self._client_context, "jp front SPACE")
        self.assertEqual(response, '日本語.')

    def test_jp_middle_space(self):
        response = self._client_context.bot.ask_question(self._client_context, "jp middle SPACE")
        self.assertEqual(response, "日本語 テスト.")

    def test_jp_last_space(self):
        response = self._client_context.bot.ask_question(self._client_context, "jp last SPACE")
        self.assertEqual(response, '日本語.')

    def test_jp_space_before_tag(self):
        response = self._client_context.bot.ask_question(self._client_context, "jp SPACE before TAG")
        self.assertEqual(response, '日本語.')

    def test_jp_space_between_tag(self):
        response = self._client_context.bot.ask_question(self._client_context, "jp no SPACE between TAG")
        self.assertEqual(response, "日本語テスト.")

        response = self._client_context.bot.ask_question(self._client_context, "jp SPACE between TAG")
        self.assertEqual(response, "日本語 テスト.")

    def test_jp_space_after_tag(self):
        response = self._client_context.bot.ask_question(self._client_context, "jp SPACE after TAG")
        self.assertEqual(response, '日本語.')

    def test_en_space_jp(self):
        response = self._client_context.bot.ask_question(self._client_context, "en SPACE jp")
        self.assertEqual(response, 'Test 日本語.')

    def test_jp_space_en(self):
        response = self._client_context.bot.ask_question(self._client_context, "jp SPACE en")
        self.assertEqual(response, '日本語 test.')

    def test_tag_en_space_jp(self):
        response = self._client_context.bot.ask_question(self._client_context, "TAG en jp")
        self.assertEqual(response, 'Testテスト.')

        response = self._client_context.bot.ask_question(self._client_context, "TAG en SPACE jp")
        self.assertEqual(response, 'Test テスト.')

    def test_tag_jp_space_en(self):
        response = self._client_context.bot.ask_question(self._client_context, "TAG jp en")
        self.assertEqual(response, 'テストtest.')

        response = self._client_context.bot.ask_question(self._client_context, "TAG jp SPACE en")
        self.assertEqual(response, 'テスト test.')
