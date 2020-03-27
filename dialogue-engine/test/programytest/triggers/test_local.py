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

from programy.triggers.manager import TriggerManager
from programy.triggers.config import TriggerConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.factory import StorageFactory
from programytest.client import TestClient


class LocalTriggerManagerTests(unittest.TestCase):

    def test_load_triggers(self):
        config = TriggerConfiguration()
        config._manager = TriggerConfiguration.LOCAL_MANAGER

        mgr = TriggerManager.load_trigger_manager(config)

        trigger_file = os.path.dirname(__file__) + os.sep + "triggers.txt"
        self.assertTrue(os.path.exists(trigger_file))

        config = FileStorageConfiguration()
        config._triggers_storage = FileStoreConfiguration(file=trigger_file, format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()

        storage_factory = StorageFactory()

        storage_factory._storage_engines[StorageFactory.TRIGGERS] = engine
        storage_factory._store_to_engine_map[StorageFactory.TRIGGERS] = engine

        mgr.load_triggers(storage_factory)

        triggers = mgr.get_triggers("SYSTEM_STARTUP")
        self.assertIsNotNone(triggers)
        self.assertEquals(2, len(triggers))

        triggers = mgr.get_triggers("SYSTEM_SHUTDOWN")
        self.assertIsNotNone(triggers)
        self.assertEquals(1, len(triggers))

        triggers = mgr.get_triggers("CONVERSATION_START")
        self.assertIsNotNone(triggers)
        self.assertEquals(1, len(triggers))

    def test_trigger_triggers(self):
        config = TriggerConfiguration()
        config._manager = TriggerConfiguration.LOCAL_MANAGER

        mgr = TriggerManager.load_trigger_manager(config)

        trigger_file = os.path.dirname(__file__) + os.sep + "triggers.txt"

        config = FileStorageConfiguration()
        config._triggers_storage = FileStoreConfiguration(file=trigger_file, format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()

        storage_factory = StorageFactory()

        storage_factory._storage_engines[StorageFactory.TRIGGERS] = engine
        storage_factory._store_to_engine_map[StorageFactory.TRIGGERS] = engine

        mgr.load_triggers(storage_factory)

        client = TestClient()
        client_context = client.create_client_context("testid")

        triggered = mgr.trigger("SYSTEM_STARTUP")
        self.assertTrue(triggered)

        triggered = mgr.trigger("SYSTEM_STARTUP", additional={"key": "value"})
        self.assertTrue(triggered)

        triggered = mgr.trigger("CONVERSATION_START", client_context)
        self.assertTrue(triggered)

        triggered = mgr.trigger("OTHER_EVENT")
        self.assertFalse(triggered)

        triggered = mgr.trigger("OTHER_EVENT", client_context)
        self.assertFalse(triggered)

        triggered = mgr.trigger("OTHER_EVENT", client_context, additional={"key": "value"})
        self.assertFalse(triggered)
