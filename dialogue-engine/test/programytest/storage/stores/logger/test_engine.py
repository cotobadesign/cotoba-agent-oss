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
import unittest.mock

from programy.storage.stores.logger.engine import LoggerStorageEngine
from programy.storage.stores.logger.config import LoggerStorageConfiguration

from programytest.storage.test_utils import StorageEngineTestUtils


class LoggerStorageEngineTests(StorageEngineTestUtils):

    def test_init_with_configuration(self):
        config = unittest.mock.Mock
        engine = LoggerStorageEngine(config)
        self.assertIsNotNone(engine)
        self.assertIsNotNone(engine.configuration)

    def test_conversations(self):
        config = LoggerStorageConfiguration()
        engine = LoggerStorageEngine(config)
        engine.initialise()
        self.conversation_asserts(storage_engine=engine, visit=False)
