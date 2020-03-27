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

from programy.storage.stores.nosql.redis.store.errors import RedisErrorsStore
from programy.storage.stores.nosql.redis.engine import RedisStorageEngine
from programy.storage.stores.nosql.redis.config import RedisStorageConfiguration

import programytest.storage.engines as Engines


class RedisErrorseStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisErrorsStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_save_errors(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisErrorsStore(engine)

        errors = [["aiml1.xml", "10", "20", "1", "5", "node", "Error_1"]]
        store.save_errors(errors)

    def test_load_errors(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisErrorsStore(engine)

        errors = [["aiml1.xml", "10", "20", "1", "5", "node", "Error_1"]]
        store.save_errors(errors)

        errorInfo = store.load_errors()
        self.assertIsNotNone(errorInfo)
        self.assertIsNotNone(errorInfo['errors'])
        errors = errorInfo['errors']
        error = errors[0]
        self.assertEqual("aiml1.xml", error['file'])

    def test_load_errors_no_redis(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisErrorsStore(engine)

        errorInfo = store.load_errors()
        self.assertIsNone(errorInfo)
