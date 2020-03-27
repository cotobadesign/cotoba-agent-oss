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
import re
import os

from programy.dialog.tokenizer.tokenizer_jp import TokenizerJP
from programy.mappings.gender import GenderCollection
from programy.storage.factory import StorageFactory
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStoreConfiguration


class GenderiseTests(unittest.TestCase):

    def test_initialise_collection(self):
        collection = GenderCollection()
        self.assertIsNotNone(collection)

    def test_collection_operations(self):
        collection = GenderCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup("with him", 'with her')

        self.assertTrue(collection.has_keyVal("WITH HIM"))
        self.assertEqual('with her', collection.value("WITH HIM"))

        self.assertEqual(collection.gender("WITH HIM"), 'with her')
        self.assertEqual(collection.genderise_string(None, "This is with him"), "This is with her")

    def test_collection_invalid(self):
        collection = GenderCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup("with him", 'with her')

        self.assertFalse(collection.has_keyVal("WITH YOU"))
        self.assertIsNone(collection.value("WITH YOU"))

        self.assertIsNone(collection.gender("WITH YOU"))
        self.assertEqual(collection.genderise_string(None, "This is with you"), "This is with you")

    def test_collection_duplicate(self):
        collection = GenderCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup("with him", 'with her')
        collection.add_to_lookup("with him", 'with you')

        self.assertEqual(collection.gender("WITH HIM"), 'with her')

    def test_load(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._gender_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "gender.txt",
                                                                   format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.GENDER] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.GENDER] = storage_engine

        collection = GenderCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertEqual(collection.gender("WITH HIM"), 'with her')
        self.assertEqual(collection.genderise_string(None, "This is with him"), "This is with her")

    def test_reload(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._gender_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "gender.txt",
                                                                   format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.GENDER] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.GENDER] = storage_engine

        collection = GenderCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertEqual(collection.gender("WITH HIM"), 'with her')
        self.assertEqual(collection.genderise_string(None, "This is with him"), "This is with her")

        collection.reload(storage_factory)

        self.assertEqual(collection.gender("WITH HIM"), 'with her')
        self.assertEqual(collection.genderise_string(None, "This is with him"), "This is with her")

    def test_collection_operations_JP(self):
        collection = GenderCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup("彼", '彼女')
        tokenizer = TokenizerJP()

        self.assertTrue(collection.has_keyVal("彼"))
        self.assertEqual('彼女', collection.value("彼"))

        self.assertEqual(collection.gender("彼"), '彼女')
        self.assertEqual(collection.genderise_string(tokenizer, "彼が来た"), "彼女が来た")

    def test_collection_invalid_JP(self):
        collection = GenderCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup("彼", '彼女')

        self.assertFalse(collection.has_keyVal("彼氏"))
        self.assertIsNone(collection.value("彼氏"))

        tokenizer = TokenizerJP()
        self.assertIsNone(collection.gender("彼氏"))
        self.assertEqual(collection.genderise_string(tokenizer, "彼氏が来た"), "彼氏が来た")

    def test_collection_duplicate_jp(self):
        collection = GenderCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup("彼", '彼女')
        collection.add_to_lookup("彼", '彼氏')

        self.assertEqual(collection.gender("彼"), '彼女')

    def test_load_jp(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._gender_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "gender_jp.txt",
                                                                   format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)
        tokenizer = TokenizerJP()

        storage_factory._storage_engines[StorageFactory.GENDER] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.GENDER] = storage_engine

        collection = GenderCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertEqual(collection.gender("彼"), '彼女')
        self.assertEqual(collection.genderise_string(tokenizer, "彼が来た"), "彼女が来た")

    def test_reload_jp(self):
        storage_factory = StorageFactory()
        tokenizer = TokenizerJP()

        file_store_config = FileStorageConfiguration()
        file_store_config._gender_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "gender_jp.txt",
                                                                   format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.GENDER] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.GENDER] = storage_engine

        collection = GenderCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertEqual(collection.gender("彼"), '彼女')
        self.assertEqual(collection.genderise_string(tokenizer, "彼が来た"), "彼女が来た")

        collection.reload(storage_factory)

        self.assertEqual(collection.gender("彼"), '彼女')
        self.assertEqual(collection.genderise_string(tokenizer, "彼が来た"), "彼女が来た")
