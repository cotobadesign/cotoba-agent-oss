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
import os.path
import shutil

from programy.storage.stores.file.store.logs import FileLogsStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration

from programy.dialog.conversation import Conversation

from programytest.client import TestClient


class FileLogsStoreTests(unittest.TestCase):

    def setUp(self):
        self._tmpdir = os.path.dirname(__file__) + os.sep + "logs"

    def tearDown(self):
        if os.path.exists(self._tmpdir):
            shutil.rmtree(self._tmpdir)
        self.assertFalse(os.path.exists(self._tmpdir))

    def test_initialise(self):
        config = FileStorageConfiguration()
        config.conversation_storage._dirs = [self._tmpdir]

        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLogsStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_store_logs(self):
        self.tearDown()

        config = FileStorageConfiguration()
        config.logs_storage._dirs = [self._tmpdir]

        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLogsStore(engine)
        self.assertEqual(store.storage_engine, engine)

        store.empty()

        client = TestClient()
        client_context = client.create_client_context("user1")
        conversation = Conversation(client_context)

        error_log = {"error": "logger ERROR log"} 
        warning_log = {"warning": "logger WARNING log"} 
        info_log = {"info": "logger INFO log"} 
        debug_log = {"debug": "logger DEBUG log"} 

        conversation.append_log(error_log) 
        conversation.append_log(warning_log) 
        conversation.append_log(info_log) 
        conversation.append_log(debug_log) 

        store.store_logs(client_context, conversation)

        store.empty()

    def test_load_logs(self):
        self.tearDown()

        config = FileStorageConfiguration()
        config.logs_storage._dirs = [self._tmpdir]

        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLogsStore(engine)
        self.assertEqual(store.storage_engine, engine)

        store.empty()

        client = TestClient()
        client_context = client.create_client_context("user1")
        conversation = Conversation(client_context)

        error_log = {"error": "logger ERROR log"} 
        warning_log = {"warning": "logger WARNING log"} 
        info_log = {"info": "logger INFO log"} 
        debug_log = {"debug": "logger DEBUG log"} 

        conversation.append_log(error_log) 
        conversation.append_log(warning_log) 
        conversation.append_log(info_log) 
        conversation.append_log(debug_log) 

        store.store_logs(client_context, conversation)

        logInfo = store.load_logs(client_context)
        self.assertIsNotNone(logInfo)
        logs = logInfo['logs']
        self.assertIsNotNone(logs)
        self.assertEqual(4, len(logs))
        self.assertEqual({"error": "logger ERROR log"}, logs[0])

        store.empty()

    def test_load_logs_no_file(self):
        config = FileStorageConfiguration()
        config.logs_storage._dirs = [self._tmpdir]

        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLogsStore(engine)
        self.assertEqual(store.storage_engine, engine)

        client = TestClient()
        client_context = client.create_client_context("user1")

        logs = store.load_logs(client_context)
        self.assertIsNone(logs)
