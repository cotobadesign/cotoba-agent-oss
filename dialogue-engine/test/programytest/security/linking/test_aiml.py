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

from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.security.linking.accountlinker import BasicAccountLinkerService

from programytest.client import TestClient


class AccountLinkerTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(AccountLinkerTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class AccountLinkerAIMLTests(unittest.TestCase):

    def setUp(self):
        config = SQLStorageConfiguration()
        storage_engine = SQLStorageEngine(config)
        storage_engine.initialise()

        client = AccountLinkerTestClient()
        self.context = client.create_client_context("TESTUSER")
        self.context.brain._security._account_linker = BasicAccountLinkerService(storage_engine)

    def test_account_link_happy_path(self):
        response = self.context.bot.ask_question(self.context,  "LINK PRIMARY ACCOUNT USER1 CONSOLE PASSWORD123")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith('Your generated key is'))

        words = response.split(" ")
        self.assertTrue(5, len(words))
        generated_key = words[4][:-1]

        command = "LINK SECONDARY ACCOUNT USER1 USER2 FACEBOOK PASSWORD123 %s" % generated_key
        response = self.context.bot.ask_question(self.context,  command)
        self.assertIsNotNone(response)
        self.assertEqual('Your accounts are now linked.', response)
