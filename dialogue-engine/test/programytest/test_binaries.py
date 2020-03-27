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
import shutil

from programy.binaries import BinariesManager
from programy.config.brain.binaries import BrainBinariesConfiguration
from programy.parser.aiml_parser import AIMLParser
from programy.storage.factory import StorageFactory
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.binaries import FileBinariesStore
from programy.storage.stores.file.store.config import FileStoreConfiguration

from programytest.client import TestClient


class BinariesTestClient(TestClient):

    TEST_AIML_FILE = "testdata" + os.sep + "basic.aiml"

    def __init__(self, filename, save_bin=False, load_bin=False):
        self._filename = filename
        self._save_bin = save_bin
        self._load_bin = load_bin
        TestClient.__init__(self)

    def load_storage(self):
        super(BinariesTestClient, self).load_storage()
        self.add_default_stores()

        bot_config = self.configuration.client_configuration.configurations[0]
        brain_config = bot_config.configurations[0]
        brain_config.binaries._load_binary = self._load_bin
        brain_config.binaries._save_binary = self._save_bin

        aimlfile = os.path.dirname(__file__) + os.sep + self.TEST_AIML_FILE
        self._file_store_config._categories_storage = FileStoreConfiguration(dirs=aimlfile, format="xml", extension="aiml", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.CATEGORIES] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.CATEGORIES] = self._storage_engine

        config = FileStoreConfiguration()
        config._dirs = [self._filename]
        config._has_single_file = True
        self._file_store_config._binaries_storage = config
        self.storage_factory._storage_engines[StorageFactory.BINARIES] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.BINARIES] = self._storage_engine


class BinariesTests(unittest.TestCase):

    TEST_DIRECTORY = "tmp"

    def setUp(self):
        tmpdir = os.path.dirname(__file__) + os.sep + self.TEST_DIRECTORY
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)

    def test_botclient_binary_save(self):
        tmpdir = os.path.dirname(__file__) + os.sep + "tmp"
        binfile = tmpdir + os.sep + 'braintree.bin'

        BinariesTestClient(binfile, save_bin=True)
        self.assertTrue(os.path.exists(binfile))

        tmpdir = os.path.dirname(__file__) + os.sep + self.TEST_DIRECTORY
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)

    def test_botclient_binary_load(self):
        tmpdir = os.path.dirname(__file__) + os.sep + "tmp"
        binfile = tmpdir + os.sep + 'braintree.bin'

        BinariesTestClient(binfile, save_bin=True)
        self.assertTrue(os.path.exists(binfile))

        BinariesTestClient(binfile, load_bin=True)
        self.assertTrue(os.path.exists(binfile))

        tmpdir = os.path.dirname(__file__) + os.sep + self.TEST_DIRECTORY
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)

    def test_botclient_binary_load_no_data(self):
        tmpdir = os.path.dirname(__file__) + os.sep + "tmp"
        binfile = tmpdir + os.sep + 'braintree.bin'

        BinariesTestClient(binfile, load_bin=True)
        self.assertFalse(os.path.exists(binfile))

    def test_botclient_binary_save_and_load(self):
        tmpdir = os.path.dirname(__file__) + os.sep + "tmp"
        binfile = tmpdir + os.sep + 'braintree.bin'

        BinariesTestClient(binfile, save_bin=True)
        self.assertTrue(os.path.exists(binfile))

        BinariesTestClient(binfile, save_bin=True, load_bin=True)
        self.assertTrue(os.path.exists(binfile))

        tmpdir = os.path.dirname(__file__) + os.sep + self.TEST_DIRECTORY
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)

    def test_load_binary_no_storage(self):
        bin_config = BrainBinariesConfiguration()
        bin_manager = BinariesManager(bin_config)
        storage_factory = StorageFactory()

        bin_manager.load_binary(storage_factory)

    def test_save_binary_no_parser(self):
        bin_config = BrainBinariesConfiguration()
        bin_manager = BinariesManager(bin_config)
        storage_factory = StorageFactory()

        bin_manager.save_binary(storage_factory)

    def test_save_binary_no_storage(self):
        bin_config = BrainBinariesConfiguration()
        bin_manager = BinariesManager(bin_config)

        tmpdir = os.path.dirname(__file__) + os.sep + "tmp"
        binfile = tmpdir + os.sep + 'braintree.bin'

        client = TestClient(binfile)

        bot = client.bot_factory._bots['bot']
        brain = bot.brain

        bin_manager.set_aiml_parser(brain.aiml_parser)
        bin_manager.save_binary(client.storage_factory)
