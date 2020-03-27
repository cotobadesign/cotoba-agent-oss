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
import json

from src.programy.nlu.nlu import NluRequest
from src.programy.storage.stores.file.store.config import FileStoreConfiguration
from src.programy.storage.factory import StorageFactory

from programytest.client import TestClient


class DummyNlu(NluRequest):

    def set_request_api(self, api):
        pass

    def nluCall(self, client_context, url, apikey, utterance):
        nlu_result_a = """{
            "intents": [
                {"intent": "transportation", "score":
        """
        nlu_result_b = """},
                {"intent": "aroundsearch", "score": 0.8 }
                ],
            "slots": [
                {"slot": "departure", "entity": "東京", "score": 0.85, "startOffset": 3, "endOffset": 5 }
                ]
            }
        """

        nlu_result = nlu_result_a + ' ' + apikey + nlu_result_b
        json_data = json.loads(nlu_result, encoding='utf_8')
        result = json.dumps(json_data)

        return result


class NluIntentTestClient(TestClient):

    def __init__(self, aiml_file, score):
        self._aiml_file = aiml_file
        self._score = score
        TestClient.__init__(self)

    def load_storage(self):
        super(NluIntentTestClient, self).load_storage()
        self.add_default_stores()

        aimlfile = os.path.dirname(__file__) + os.sep + self._aiml_file
        self._file_store_config._categories_storage = FileStoreConfiguration(dirs=aimlfile, format="xml", extension="aiml", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.CATEGORIES] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.CATEGORIES] = self._storage_engine

        bot_config = self.configuration.client_configuration.configurations[0]
        brain_config = bot_config._brain_configs[0]
        brain_config.nlu._classname = 'programytest.aiml_tests.nlu_tests.test_nlu_intent.DummyNlu'
        brain_config.nlu._url = 'http://test_nlu.co.jp'
        brain_config.nlu._apikey = self._score
        brain_config.nlu._use_file = False


class NluIntentTests(unittest.TestCase):

    def test_nluintent(self):
        client = NluIntentTestClient('nlu_intent.aiml', '0.9')
        self._client_context = client.create_client_context("testid")

        self.assertIsNotNone(self._client_context.brain.nlu)

        response = self._client_context.bot.ask_question(self._client_context, "Match NLU")
        self.assertIsNotNone(response)
        self.assertEqual(response, "NLU result 0.8.")

    def test_nluintent_with_tag(self):
        client = NluIntentTestClient('nlu_intent.aiml', '0.8')
        self._client_context = client.create_client_context("testid")

        self.assertIsNotNone(self._client_context.brain.nlu)

        response = self._client_context.bot.ask_question(self._client_context, "Match NLU")
        self.assertIsNotNone(response)
        self.assertEqual(response, "NLU result 0.8.")

    def test_nluintent_with_index(self):
        client = NluIntentTestClient('nlu_intent.aiml', '0.7')
        self._client_context = client.create_client_context("testid")

        self.assertIsNotNone(self._client_context.brain.nlu)

        response = self._client_context.bot.ask_question(self._client_context, "Match NLU")
        self.assertIsNotNone(response)
        self.assertEqual(response, "NLU result unknown.")

    def test_nluintent_wildcard(self):
        client = NluIntentTestClient('nlu_intent.aiml', '0.6')
        self._client_context = client.create_client_context("testid")

        self.assertIsNotNone(self._client_context.brain.nlu)

        response = self._client_context.bot.ask_question(self._client_context, "Match NLU")
        self.assertIsNotNone(response)
        self.assertEqual(response, "NLU result 0.6.")

    def test_nluintent_widcard_with_index(self):
        client = NluIntentTestClient('nlu_intent.aiml', '0.5')
        self._client_context = client.create_client_context("testid")

        self.assertIsNotNone(self._client_context.brain.nlu)

        response = self._client_context.bot.ask_question(self._client_context, "Match NLU")
        self.assertIsNotNone(response)
        self.assertEqual(response, "NLU result 0.8.")

    def test_nluintent_invlid_name(self):
        client = NluIntentTestClient('nlu_intent.aiml', '0.4')
        self._client_context = client.create_client_context("testid")

        self.assertIsNotNone(self._client_context.brain.nlu)

        response = self._client_context.bot.ask_question(self._client_context, "Match NLU")
        self.assertIsNotNone(response)
        self.assertEqual(response, "NLU result unknown.")
