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

from programy.braintree import BraintreeManager
from programy.config.brain.braintree import BrainBraintreeConfiguration
from programy.storage.stores.file.store.config import FileStoreConfiguration
from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.factory import StorageFactory

from programytest.client import TestClient


class BrainTreeTestClient(TestClient):

    TEST_AIML_FILE = "testdata" + os.sep + "basic.aiml"

    def __init__(self, tree_type='xml', filename=None):
        self._tree_type = tree_type
        self._filename = filename
        TestClient.__init__(self)

    def load_storage(self):
        super(BrainTreeTestClient, self).load_storage()
        self.add_default_stores()

        aimlfile = os.path.dirname(__file__) + os.sep + self.TEST_AIML_FILE
        self._file_store_config._categories_storage = FileStoreConfiguration(dirs=aimlfile, format="xml", extension="aiml", encoding="utf-8", delete_on_start=False)
        self.storage_factory._storage_engines[StorageFactory.CATEGORIES] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.CATEGORIES] = self._storage_engine

        config = FileStoreConfiguration()
        config._format = self._tree_type
        config._dirs = [self._filename]
        config._has_single_file = True
        self._file_store_config._braintree_storage = config
        self.storage_factory._storage_engines[StorageFactory.BRAINTREE] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.BRAINTREE] = self._storage_engine


class BrainTreeTests(unittest.TestCase):

    TEST_DIRECTORY = "tmp"

    def setUp(self):
        tmpdir = os.path.dirname(__file__) + os.sep + self.TEST_DIRECTORY
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)

    def test_dump_brain_tree(self):
        tmpdir = os.path.dirname(__file__) + os.sep + self.TEST_DIRECTORY
        treefile = tmpdir + os.sep + 'braintree.xml'

        client = BrainTreeTestClient(tree_type=FileStore.XML_FORMAT, filename=treefile)
        client_context = client.create_client_context("testid")

        configure = BrainBraintreeConfiguration()
        configure._create = True

        braintree = BraintreeManager(configure)
        braintree.dump_brain_tree(client_context)
        self.assertTrue(os.path.exists(treefile))

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_dump_brain_tree_txt(self):
        tmpdir = os.path.dirname(__file__) + os.sep + self.TEST_DIRECTORY
        treefile = tmpdir + os.sep + 'braintree.txt'

        client = BrainTreeTestClient(tree_type=FileStore.TEXT_FORMAT, filename=treefile)
        client_context = client.create_client_context("testid")

        configure = BrainBraintreeConfiguration()
        configure._create = True

        braintree = BraintreeManager(configure)
        braintree.dump_brain_tree(client_context)
        self.assertTrue(os.path.exists(treefile))

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_dump_brain_tree_invalid(self):
        tmpdir = os.path.dirname(__file__) + os.sep + self.TEST_DIRECTORY
        treefile = tmpdir + os.sep + 'braintree.csv'

        client = BrainTreeTestClient(tree_type=FileStore.CSV_FORMAT, filename=treefile)
        client_context = client.create_client_context("testid")

        configure = BrainBraintreeConfiguration()
        configure._create = True

        braintree = BraintreeManager(configure)
        braintree.dump_brain_tree(client_context)
        self.assertFalse(os.path.exists(treefile))

    def test_dump_brain_tree_no_storage(self):
        tmpdir = os.path.dirname(__file__) + os.sep + self.TEST_DIRECTORY
        treefile = tmpdir + os.sep + 'braintree.xml'

        client = TestClient()
        client_context = client.create_client_context("testid")

        configure = BrainBraintreeConfiguration()
        configure._create = True

        braintree = BraintreeManager(configure)
        braintree.dump_brain_tree(client_context)
        self.assertFalse(os.path.exists(treefile))
