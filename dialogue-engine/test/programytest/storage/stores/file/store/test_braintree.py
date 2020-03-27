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

from programy.storage.stores.file.store.braintree import FileBraintreeStore
from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.store.config import FileStoreConfiguration
from programytest.client import TestClient


class FileBraintreeStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileBraintreeStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_save_braintree_xml_format(self):
        config = FileStorageConfiguration()
        config._categories_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "categories"],
                                                            extension="aiml", subdirs=False, format="xml", encoding="utf-8", delete_on_start=False)
        tmpdir = os.path.dirname(__file__) + os.sep + "braintree"
        tmpfile = tmpdir + os.sep + "braintree.xml"
        config.braintree_storage._dirs = [tmpfile]
        config.braintree_storage._has_single_file = True
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileBraintreeStore(engine)

        path = store._get_dir_from_path(store._get_storage_path())
        if os.path.exists(path):
            shutil.rmtree(path)
        self.assertFalse(os.path.exists(path))

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")
        pattern_graph = client_context.brain.aiml_parser.pattern_parser

        store.save_braintree(client_context, pattern_graph)

        self.assertTrue(os.path.exists(store._get_storage_path()))

        shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_save_braintree_text_format(self):
        config = FileStorageConfiguration()
        config._categories_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "categories"],
                                                            extension="aiml", subdirs=False, format="xml", encoding="utf-8", delete_on_start=False)
        tmpdir = os.path.dirname(__file__) + os.sep + "braintree"
        tmpfile = tmpdir + os.sep + "braintree.txt"
        config.braintree_storage._format = FileStore.TEXT_FORMAT
        config.braintree_storage._dirs = [tmpfile]
        config.braintree_storage._has_single_file = True
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileBraintreeStore(engine)

        path = store._get_dir_from_path(store._get_storage_path())
        if os.path.exists(path):
            shutil.rmtree(path)
        self.assertFalse(os.path.exists(path))

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")
        pattern_graph = client_context.brain.aiml_parser.pattern_parser

        store.save_braintree(client_context, pattern_graph)

        self.assertTrue(os.path.exists(store._get_storage_path()))

        shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_save_braintree_invalid_format(self):
        config = FileStorageConfiguration()
        config._categories_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "categories"],
                                                            extension="aiml", subdirs=False, format="xml", encoding="utf-8", delete_on_start=False)
        tmpdir = os.path.dirname(__file__) + os.sep + "braintree"
        tmpfile = tmpdir + os.sep + "braintree.csv"
        config.braintree_storage._format = FileStore.CSV_FORMAT
        config.braintree_storage._dirs = [tmpfile]
        config.braintree_storage._has_single_file = True
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileBraintreeStore(engine)

        path = store._get_dir_from_path(store._get_storage_path())
        if os.path.exists(path):
            shutil.rmtree(path)
        self.assertFalse(os.path.exists(path))

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")
        pattern_graph = client_context.brain.aiml_parser.pattern_parser

        store.save_braintree(client_context, pattern_graph)
        self.assertFalse(os.path.exists(store._get_storage_path()))
