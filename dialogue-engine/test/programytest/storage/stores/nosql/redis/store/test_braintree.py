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

from programy.storage.stores.nosql.redis.store.braintree import RedisBraintreeStore
from programy.storage.stores.nosql.redis.store.redisstore import RedisStore
from programy.storage.stores.nosql.redis.engine import RedisStorageEngine
from programy.storage.stores.nosql.redis.config import RedisStorageConfiguration
from programytest.client import TestClient


class RedisBraintreeStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisBraintreeStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_save_braintree_xml_format(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisBraintreeStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")
        pattern_graph = client_context.brain.aiml_parser.pattern_parser

        store.save_braintree(client_context, pattern_graph)

    """
    def test_save_braintree_text_format(self):
        config = RedisStorageConfiguration()
        config.braintree_storage._format = RedisStore.TEXT_FORMAT
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisBraintreeStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")
        pattern_graph = client_context.brain.aiml_parser.pattern_parser

        store.save_braintree(client_context, pattern_graph)
    """

    """
    def test_save_braintree_invalid_format(self):
        config = RedisStorageConfiguration()
        config.braintree_storage._format = RedisStore.CSV_FORMAT
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisBraintreeStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")
        pattern_graph = client_context.brain.aiml_parser.pattern_parser

        store.save_braintree(client_context, pattern_graph)
    """
