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

from programy.nlu.nlu import NluRequest
from programy.clients.restful.client import UserInfo
from programy.parser.aiml_parser import AIMLLoader, AIMLParser
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.store.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.factory import StorageFactory

from programytest.client import TestClient


class InvalidNlu(NluRequest):

    def set_request_api(self, api):
        pass


class DummyNlu(NluRequest):

    def set_request_api(self, api):
        pass

    def nluCall(self, client_context, url, apikey, utternce, timeout=None):
        nlu_result_1 = """{
            "intents": [
                {"intent": "transportation", "score": 0.9 },
                {"intent": "aroundsearch", "score": 0.8 }
                ],
            "slots": [
                {"slot": "departure", "entity": "東京", "score": 0.85, "startOffset": 3, "endOffset": 5 },
                {"slot": "arrival", "entity": "京都", "score": 0.86, "startOffset": 8, "endOffset": 10 },
                {"slot": "departure_time", "entity": "2018/11/1 19:00", "score": 0.87, "startOffset": 12, "endOffset": 14 },
                {"slot": "arrival_time", "entity": "2018/11/1 11:00", "score": 0.88, "startOffset": 13, "endOffset": 18 }
                ]
            }
        """
        nlu_result_2 = """{
            "intents": [
                {"intent": "aroundsearch", "score": 0.8 }
                ],
            "slots": [
                {"slot": "arrival_time", "entity": "2018/11/1 11:00", "score": 0.88, "startOffset": 13, "endOffset": 18 }
                ]
            }
        """
        nlu_result_3 = """{
            "intents": [
                {"intent": "transportation", "score": 0.91 }
                ],
            "slots": [
                {"slot": "departure", "entity": "東京", "score": 0.85, "startOffset": 3, "endOffset": 5 }
                ]
            }
        """
        nlu_result_4 = """{
            "intents": [
                {"intent": "transportation", "score": 0.89 }
                ],
            "slots": [
                {"slot": "departure", "entity": "東京", "score": 0.85, "startOffset": 3, "endOffset": 5 }
                ]
            }
        """

        if apikey == '1':
            json_data = json.loads(nlu_result_1, encoding='utf_8')
            result = json.dumps(json_data)
        elif apikey == '2':
            json_data = json.loads(nlu_result_2, encoding='utf_8')
            result = json.dumps(json_data)
        elif apikey == '3':
            json_data = json.loads(nlu_result_3, encoding='utf_8')
            result = json.dumps(json_data)
        elif apikey == '4':
            json_data = json.loads(nlu_result_4, encoding='utf_8')
            result = json.dumps(json_data)
        else:
            result = None

        return result


class NluTestClient(TestClient):

    def __init__(self, aiml_file, response_type=None, nlu_invalid=False):
        self._aiml_file = aiml_file
        self._response_type = response_type
        self._nlu_invalid = nlu_invalid
        TestClient.__init__(self)

    def load_storage(self):
        super(NluTestClient, self).load_storage()
        self.add_default_stores()

        aimlfile = os.path.dirname(__file__) + os.sep + self._aiml_file
        self._file_store_config._categories_storage = FileStoreConfiguration(dirs=aimlfile, format="xml", extension="aiml", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.CATEGORIES] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.CATEGORIES] = self._storage_engine

        bot_config = self.configuration.client_configuration.configurations[0]
        brain_config = bot_config._brain_configs[0]
        if self._nlu_invalid is False:
            brain_config.nlu._classname = 'programytest.aiml_tests.nlu_tests.test_nlu.DummyNlu'
        else:
            brain_config.nlu._classname = 'programytest.aiml_tests.nlu_tests.test_nlu.InvalidNlu'
        brain_config.nlu._url = 'http://test_nlu.co.jp'
        brain_config.nlu._apikey = self._response_type
        brain_config.nlu._use_file = False


class BrainNLUTests(unittest.TestCase):

    def test_nlu_response(self):
        client = NluTestClient('nlu.aiml', response_type='1')
        self._client_context = client.create_client_context("testid")

        self.assertIsNotNone(self._client_context.brain.nlu)

        response = self._client_context.bot.ask_question(self._client_context, "Match NLU")
        self.assertIsNotNone(response)
        self.assertEqual(response, "NLU transportation.")

    def test_nlu_response_with_score_gt(self):
        client = NluTestClient('nlu.aiml', response_type='3')
        self._client_context = client.create_client_context("testid")

        self.assertIsNotNone(self._client_context.brain.nlu)

        response = self._client_context.bot.ask_question(self._client_context, "Match NLU")
        self.assertIsNotNone(response)
        self.assertEqual(response, "NLU transportation GT 0.9.")

    def test_nlu_response_with_score_lt(self):
        client = NluTestClient('nlu.aiml', response_type='4')
        self._client_context = client.create_client_context("testid")

        self.assertIsNotNone(self._client_context.brain.nlu)

        response = self._client_context.bot.ask_question(self._client_context, "Match NLU")
        self.assertIsNotNone(response)
        self.assertEqual(response, "NLU transportation LT 0.9.")

    def test_none_nlu_response(self):
        client = NluTestClient('nlu.aiml')
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "No Response")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Not NLU wild-card.")

    def test_nlu_response_wildcard(self):
        client = NluTestClient('nlu.aiml', response_type='2')
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "Wild NLU")
        self.assertIsNotNone(response)
        self.assertEqual(response, "NLU wild-card.")

    def test_nlu_response_no_wildcard(self):
        client = NluTestClient('nlu_no_wildcard.aiml', response_type='2')
        self._client_context = client.create_client_context("testid")

        self._client_context.brain.properties.add_property("default-response", "unknown")

        response = self._client_context.bot.ask_question(self._client_context, "Wild NLU")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Unknown.")

    def test_not_nlu_response(self):
        client = NluTestClient('nlu.aiml')
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "None_NLU")
        self.assertIsNotNone(response)
        self.assertEqual(response, "None nlu result.")

    def test_nlu_and_srai(self):
        client = NluTestClient('nlu_srai.aiml', response_type='1')
        self._client_context = client.create_client_context("testid")
        self._client_context.userInfo = UserInfo(None, None)

        response = self._client_context.bot.ask_question(self._client_context, "Match NLU")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Ok srai.")

    def test_nlu_and_invalid_srai(self):
        client = NluTestClient('nlu_invalid_srai.aiml', response_type='1')
        self._client_context = client.create_client_context("testid")
        self._client_context.userInfo = UserInfo(None, None)

        response = self._client_context.bot.ask_question(self._client_context, "Match NLU")
        self.assertIsNotNone(response)
        self.assertEqual(response, "")

    def test_nlu_not_implemets(self):
        client = NluTestClient('nlu.aiml', response_type='1', nlu_invalid=True)
        self._client_context = client.create_client_context("testid")

        response = self._client_context.bot.ask_question(self._client_context, "Match NLU")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Not NLU wild-card.")
