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
from programytest.storage.asserts.store.assert_conversations import ConverstionStoreAsserts

from programy.storage.stores.nosql.redis.store.conversations import RedisConversationStore
from programy.storage.stores.nosql.redis.engine import RedisStorageEngine
from programy.storage.stores.nosql.redis.config import RedisStorageConfiguration

from programy.dialog.conversation import Conversation

from programytest.client import TestClient


class RedisConversationStoreTests(ConverstionStoreAsserts):

    def test_initialise(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def tests_conversation_storage(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_conversation_storage(store, can_empty=True, test_load=True)

    def tests_conversation_storage_no_file(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        client = TestClient()
        client_context = client.create_client_context("user1")
        conversation = Conversation(client_context)

        store.load_conversation(client_context, conversation)
        self.assertEqual(0, len(conversation.questions))

    def tests_debug_conversation(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_debug_conversation(store)

    def tests_debug_conversation_no_file(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        client = TestClient()
        client_context = client.create_client_context("user1")

        debugInfo, _ = store.debug_conversation_data(client_context)
        self.assertEqual(0, len(debugInfo))

    def tests_modify_conversation(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_modify_conversation_data(store)
