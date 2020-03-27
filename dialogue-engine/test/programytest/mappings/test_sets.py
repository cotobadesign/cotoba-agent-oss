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

from programy.mappings.sets import SetCollection
from programy.storage.factory import StorageFactory
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStoreConfiguration


class SetTests(unittest.TestCase):

    def test_initialise_collection(self):
        collection = SetCollection()
        self.assertIsNotNone(collection)
        self.assertIsNotNone(collection.sets)
        self.assertIsNotNone(collection.stores)
        self.assertIsNotNone(collection.is_cjk)

    def test_collection_operations(self):
        collection = SetCollection()
        set_dict = {"A": [["A", "A B", "A C"]], "D": [["D"]], "E": [["E", "E F"]]}
        values = {"A": "A", "A B": "A B", "A C": "A C", "D": "D", "E": "E", "E F": "E F"}
        collection.add_set("TESTSET", set_dict, "teststore", False, values)
        set_dict = {"1": [["1", "1 2", "1 3"]], "4": [["4"]], "5": [["5", "5 6"]]}
        values = {"1": "1", "1 2": "1 2", "1 3": "1 3", "4": "4", "5": "5", "5 6": "5 6"}
        collection.add_set("TESTSET2", set_dict, "teststore", False, values)

        self.assertIsNotNone(collection.sets)
        self.assertIsNotNone(collection.stores)

        self.assertTrue(collection.contains("TESTSET"))
        self.assertTrue(collection.contains("TESTSET2"))
        self.assertFalse(collection.contains("TESTSET3"))
        self.assertEqual(collection.store_name("TESTSET"), "teststore")
        self.assertEqual(collection.store_name("TESTSET2"), "teststore")
        self.assertIsNone(collection.store_name("TESTSET3"))
        self.assertFalse(collection.is_cjk("TESTSET"))
        self.assertFalse(collection.is_cjk("TESTSET2"))
        self.assertIsNone(collection.is_cjk("TESTSET3"))

        aset = collection.set_list("TESTSET")
        self.assertIsNotNone(aset)

        self.assertEqual(12, collection.count_words_in_sets())

        collection.remove("TESTSET2")
        self.assertTrue(collection.contains("TESTSET"))
        self.assertFalse(collection.contains("TESTSET2"))
        self.assertFalse(collection.contains("TESTSET3"))

        collection.empty()

        self.assertIsNotNone(collection.sets)
        self.assertIsNotNone(collection.stores)

        self.assertFalse(collection.contains("TESTSET"))
        self.assertIsNone(collection.set_list("TESTSET"))
        self.assertNotEquals(collection.store_name("TESTSET"), "teststore")

    def test_collection_operations_jp(self):
        collection = SetCollection()
        set_dict = {"千": ["千葉", "千葉県"], "東": ["東京", "東京都"]}
        values = {"千葉": "千葉", "千葉県": "千葉県", "東京": "東京", "東京都": "東京都"}
        collection.add_set("TESTSET", set_dict, "teststore", True, values)
        set_dict = {"神": ["神奈川", "神戸", "神田"], "大": ["大阪", "大分", "大津"]}
        values = {"神奈川": "神奈川", "神戸": "神戸", "神田": "神田", "大阪": "大阪", "大分": "大分", "大津": "大津"}
        collection.add_set("TESTSET2", set_dict, "teststore", True, values)

        self.assertIsNotNone(collection.sets)
        self.assertIsNotNone(collection.stores)

        self.assertTrue(collection.contains("TESTSET"))
        self.assertTrue(collection.contains("TESTSET2"))
        self.assertFalse(collection.contains("TESTSET3"))
        self.assertEqual(collection.store_name("TESTSET"), "teststore")
        self.assertEqual(collection.store_name("TESTSET2"), "teststore")
        self.assertIsNone(collection.store_name("TESTSET3"))
        self.assertTrue(collection.is_cjk("TESTSET"))
        self.assertTrue(collection.is_cjk("TESTSET2"))
        self.assertIsNone(collection.is_cjk("TESTSET3"))

        aset = collection.set_list("TESTSET")
        self.assertIsNotNone(aset)

        self.assertEqual(10, collection.count_words_in_sets())

        collection.remove("TESTSET2")
        self.assertTrue(collection.contains("TESTSET"))
        self.assertFalse(collection.contains("TESTSET2"))
        self.assertFalse(collection.contains("TESTSET3"))

        collection.empty()

        self.assertIsNotNone(collection.sets)
        self.assertIsNotNone(collection.stores)

        self.assertFalse(collection.contains("TESTSET"))
        self.assertIsNone(collection.set_list("TESTSET"))
        self.assertNotEquals(collection.store_name("TESTSET"), "teststore")

    def test_collection_duplicate(self):
        collection = SetCollection()
        set_dict = {"A": [["A", "A B", "A C"]], "D": [["D"]], "E": [["E", "E F"]]}
        values = {"A": "A", "A B": "A B", "A C": "A C", "D": "D", "E": "E", "E F": "E F"}
        collection.add_set("TESTSET", set_dict, "teststore", False, values)

        with self.assertRaises(Exception):
            set_dict = {"1": [["1", "1 2", "1 3"]], "4": [["4"]], "5": [["5", "5 6"]]}
            values = {"1": "1", "1 2": "1 2", "1 3": "1 3", "4": "4", "5": "5", "5 6": "5 6"}
            collection.add_set("TESTSET", set_dict, "teststore", False, values)

    def test_load_from_file(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._sets_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "sets"])
        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.SETS] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.SETS] = storage_engine

        collection = SetCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertIsNotNone(collection._sets)
        self.assertEqual(len(collection._sets), 1)

        self.assertIsNotNone(collection._stores)
        self.assertEqual(len(collection._stores), 1)

        self.assertTrue("TEST_SET" in collection._sets)
        self.assertTrue("TEST_SET" in collection._stores)
        self.assertTrue("TEST_SET" in collection._is_cjk)

        self.assertTrue(collection.contains('TEST_SET'))
        self.assertFalse(collection.is_cjk('TEST_SET'))

        aset = collection.set_list('TEST_SET')
        self.assertIsNotNone(aset)
        values = aset['AIR']
        self.assertIsNotNone(values)
        self.assertTrue(['AIR', 'FORCE', 'BLUE'] in values)

    def test_reload_from_file(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._sets_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "sets"])
        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.SETS] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.SETS] = storage_engine

        collection = SetCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertIsNotNone(collection._sets)
        self.assertEqual(len(collection._sets), 1)

        self.assertIsNotNone(collection._stores)
        self.assertEqual(len(collection._stores), 1)

        self.assertTrue("TEST_SET" in collection._sets)
        self.assertTrue("TEST_SET" in collection._stores)
        self.assertTrue("TEST_SET" in collection._is_cjk)

        self.assertTrue(collection.contains('TEST_SET'))
        self.assertFalse(collection.is_cjk('TEST_SET'))

        aset = collection.set_list('TEST_SET')
        self.assertIsNotNone(aset)
        self.assertTrue(['AIR', 'FORCE', 'BLUE'] in aset['AIR'])

        collection.reload(storage_factory, "TEST_SET")

        self.assertIsNotNone(collection._sets)
        self.assertEqual(len(collection._sets), 1)

        self.assertIsNotNone(collection._stores)
        self.assertEqual(len(collection._stores), 1)

        self.assertTrue("TEST_SET" in collection._sets)
        self.assertTrue("TEST_SET" in collection._stores)

        self.assertTrue(collection.contains('TEST_SET'))

        self.assertIsNotNone(collection.set_list('TEST_SET'))
        self.assertTrue(['AIR', 'FORCE', 'BLUE'] in collection.set_list('TEST_SET')['AIR'])

    def test_load_from_file_jp(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._sets_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "sets_jp"])
        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.SETS] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.SETS] = storage_engine

        collection = SetCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertIsNotNone(collection._sets)
        self.assertEqual(len(collection._sets), 1)

        self.assertIsNotNone(collection._stores)
        self.assertEqual(len(collection._stores), 1)

        self.assertTrue("TEST_SET" in collection._sets)
        self.assertTrue("TEST_SET" in collection._stores)
        self.assertTrue("TEST_SET" in collection._is_cjk)

        self.assertTrue(collection.contains('TEST_SET'))
        self.assertTrue(collection.is_cjk('TEST_SET'))

        aset = collection.set_list('TEST_SET')
        self.assertIsNotNone(aset)
        values = aset['千']
        self.assertIsNotNone(values)
        self.assertEqual(['千葉', '千葉県', '千葉県下'], values)

    def test_reload_from_file_jp(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._sets_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "sets_jp"])
        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.SETS] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.SETS] = storage_engine

        collection = SetCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertIsNotNone(collection._sets)
        self.assertEqual(len(collection._sets), 1)

        self.assertIsNotNone(collection._stores)
        self.assertEqual(len(collection._stores), 1)

        self.assertTrue("TEST_SET" in collection._sets)
        self.assertTrue("TEST_SET" in collection._stores)
        self.assertTrue("TEST_SET" in collection._is_cjk)

        self.assertTrue(collection.contains('TEST_SET'))
        self.assertTrue(collection.is_cjk('TEST_SET'))

        aset = collection.set_list('TEST_SET')
        self.assertIsNotNone(aset)
        values = aset['千']
        self.assertIsNotNone(values)
        self.assertEqual(['千葉', '千葉県', '千葉県下'], values)

        collection.reload(storage_factory, "TEST_SET")

        self.assertIsNotNone(collection._sets)
        self.assertEqual(len(collection._sets), 1)

        self.assertIsNotNone(collection._stores)
        self.assertEqual(len(collection._stores), 1)

        self.assertTrue("TEST_SET" in collection._sets)
        self.assertTrue("TEST_SET" in collection._stores)

        self.assertTrue(collection.contains('TEST_SET'))

        values = aset['千']
        self.assertIsNotNone(values)
        self.assertEqual(['千葉', '千葉県', '千葉県下'], values)
