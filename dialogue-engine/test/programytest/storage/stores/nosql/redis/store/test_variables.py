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

from programytest.storage.asserts.store.assert_variables import VariablesStoreAsserts

from programy.storage.stores.nosql.redis.store.variables import RedisVariableStore
from programy.storage.stores.nosql.redis.engine import RedisStorageEngine
from programy.storage.stores.nosql.redis.config import RedisStorageConfiguration

import programytest.storage.engines as Engines


class RedisVariableStoreTests(VariablesStoreAsserts):

    @unittest.skipIf(Engines.redis is False, Engines.redis_disabled)
    def test_initialise(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisVariableStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.redis is False, Engines.redis_disabled)
    def test_variables_storage(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisVariableStore(engine)

        self.assert_variables_storage(store)

    @unittest.skipIf(Engines.redis is False, Engines.redis_disabled)
    def test_variable_storage(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisVariableStore(engine)

        self.assert_variable_storage(store)

    @unittest.skipIf(Engines.redis is False, Engines.redis_disabled)
    def test_empty_variables(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisVariableStore(engine)

        self.assert_empty_variables(store)
