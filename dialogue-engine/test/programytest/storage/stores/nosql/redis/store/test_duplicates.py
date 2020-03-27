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

from programy.storage.stores.nosql.redis.store.duplicates import RedisDuplicatesStore
from programy.storage.stores.nosql.redis.engine import RedisStorageEngine
from programy.storage.stores.nosql.redis.config import RedisStorageConfiguration

import programytest.storage.engines as Engines


class RedisDuplicatesStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisDuplicatesStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_save_duplicates(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisDuplicatesStore(engine)

        duplicates = [["aiml1.xml", "10", "20", "1", "5", "Duplicate_1"]]
        store.save_duplicates(duplicates)

    def test_load_duplicates(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisDuplicatesStore(engine)

        duplicates = [["aiml1.xml", "10", "20", "1", "5", "Duplicate_1"]]
        store.save_duplicates(duplicates)

        duplicateInfo = store.load_duplicates()
        self.assertIsNotNone(duplicateInfo)
        self.assertIsNotNone(duplicateInfo['duplicates'])
        duplicates = duplicateInfo['duplicates']
        duplicate = duplicates[0]
        self.assertEqual("aiml1.xml", duplicate['file'])

    def test_load_duplicates_no_redis(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisDuplicatesStore(engine)

        duplicateInfo = store.load_duplicates()
        self.assertIsNone(duplicateInfo)
