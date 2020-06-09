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

from programy.storage.stores.file.store.config import FileStoreConfiguration
from programy.storage.factory import StorageFactory

from programytest.client import TestClient


class JsonAIMLTestClient(TestClient):

    def __init__(self, category_file=None):
        self._category_file = category_file

        TestClient.__init__(self)

    def load_storage(self):
        super(JsonAIMLTestClient, self).load_storage()
        self.add_default_stores()

        if self._category_file is None:
            self.add_categories_store([os.path.dirname(__file__)])
        else:
            aimlfile = os.path.dirname(__file__) + os.sep + self._category_file
            self._file_store_config._categories_storage = FileStoreConfiguration(dirs=aimlfile, format="xml", extension="aiml", encoding="utf-8", delete_on_start=False)
            self.storage_factory._storage_engines[StorageFactory.CATEGORIES] = self._storage_engine
            self.storage_factory._store_to_engine_map[StorageFactory.CATEGORIES] = self._storage_engine


class JsonAIMLTests(unittest.TestCase):

    def test_json_key_variable(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON KEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Data2.")

    def test_json_joint(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON JOINT")
        self.assertIsNotNone(response)
        self.assertEqual(response, '{"key1": "data1", "key2": "data2", "key3": {"key1": "data1", "key2": "data2"}}.')

    def test_json_get_data(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON get data")
        self.assertIsNotNone(response)
        self.assertEqual(response, '{"key": "set"}.')

    def test_json_get_data_top(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON get data TOP")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Set_data Test.')

    def test_json_get_data_middle(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON get data MIDDLE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Test set_data Test.')

    def test_json_get_data_bottom(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON get data BOTTOM")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Test set_data.')

    def test_json_get_quote_data(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON get quote data")
        self.assertIsNotNone(response)
        self.assertEqual(response, '{"key": "\\"set\\""}.')

    def test_json_get_quote_top(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON get quote TOP")
        self.assertIsNotNone(response)
        self.assertEqual(response, '{"key": "\\"set\\" quote data"}.')

    def test_json_get_quote_middle(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON get quote MIDDLE")
        self.assertIsNotNone(response)
        self.assertEqual(response, '{"key": "set \\"quote\\" data"}.')

    def test_json_get_quote_bottom(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON get quote BOTTOM")
        self.assertIsNotNone(response)
        self.assertEqual(response, '{"key": "set quote \\"data\\""}.')

    def test_json_get_escape_data(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON get escape data")
        self.assertIsNotNone(response)
        self.assertEqual(response, '{"key": "\\"escape\\""}.')

    def test_json_get_list_tag(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON get list TAG")
        self.assertIsNotNone(response)
        self.assertEqual(response, '{"key": ["set", "quote", "data"]}.')

    def test_json_get_list_json(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON get list JSON")
        self.assertIsNotNone(response)
        self.assertEqual(response, '{"key": ["set", "quote", "data"]}.')

    def test_json_get_list_text(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON get list TEXT")
        self.assertIsNotNone(response)
        self.assertEqual(response, '{"key": "\\"set\\", \\"quote\\", \\"data\\""}.')

    def test_json_get_joint_tag(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON get joint tag")
        self.assertIsNotNone(response)
        self.assertEqual(response, '{"key": "set data"}.')

    def test_json_get_joint_tag_sp(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON get joint tag with sp")
        self.assertIsNotNone(response)
        self.assertEqual(response, '{"key": "set data"}.')

    def test_json_get_joint_tag_with_quote(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON get joint QUOTE")
        self.assertIsNotNone(response)
        self.assertEqual(response, '{"key": "set \\"data\\""}.')

    def test_json_get_joint_tag_with_quote_sp(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON get joint QUOTE with sp")
        self.assertIsNotNone(response)
        self.assertEqual(response, '{"key": "set \\"data\\""}.')

    def test_json_get_text_tag(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON get TEXT TAG")
        self.assertIsNotNone(response)
        self.assertEqual(response, '{"key": "answer set"}.')

    def test_json_get_text_tag_sp(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON get TEXT TAG with sp")
        self.assertIsNotNone(response)
        self.assertEqual(response, '{"key": "answer set"}.')

    def test_json_get_text_space_tag(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON get TEXT space TAG")
        self.assertIsNotNone(response)
        self.assertEqual(response, '{"key": "answer set"}.')

    def test_json_get_text_quote_tag(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON get TEXT quote TAG")
        self.assertIsNotNone(response)
        self.assertEqual(response, '{"key": "answer\\"set\\""}.')

    def test_json_get_text_quote_tag_sp(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON get TEXT quote TAG with sp")
        self.assertIsNotNone(response)
        self.assertEqual(response, '{"key": "answer\\" set\\""}.')

    def test_json_get_text_space_quote_tag(self):
        client = JsonAIMLTestClient(category_file="json.aiml")
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "JSON get TEXT space quote TAG")
        self.assertIsNotNone(response)
        self.assertEqual(response, '{"key": "answer \\"set\\""}.')
