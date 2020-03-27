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

from programy.dialog.tokenizer.tokenizer_jp import TokenizerJP
from programy.mappings.denormal import DenormalCollection
from programy.storage.factory import StorageFactory
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStoreConfiguration


class DenormaliseTests(unittest.TestCase):

    def test_initialise_collection(self):
        collection = DenormalCollection()
        self.assertIsNotNone(collection)

    def test_collection_operations(self):
        denormal_text = """
        "dot ac",".ac "
        "dot au",".au "
        "dot ca",".ca "
        "dot ch",".ch "
        "dot co",".co "
        "dot com",".com "
        """

        collection = DenormalCollection()
        self.assertIsNotNone(collection)

        collection.load_from_text(denormal_text)

        self.assertTrue(collection.has_keyVal("dot com"))
        self.assertEqual(".com ", collection.value("dot com"))

        self.assertEqual(collection.denormalise_string(None, "keithsterling dot com"), "keithsterling.com")
        self.assertIsNone(collection.denormalise("dot cox"))

    def test_collection_invalid(self):
        collection = DenormalCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup("dot com", ".com ")

        self.assertFalse(collection.has_keyVal("dot co"))
        self.assertIsNone(collection.value("dot co"))

        self.assertIsNone(collection.denormalise("dot co"))
        self.assertEqual(collection.denormalise_string(None, "www.dot.co"), "www.dot.co")

    def test_collection_duplicate(self):
        collection = DenormalCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup("dot com", ".com ")
        collection.add_to_lookup("dot com", ".co ")

        self.assertEqual(collection.denormalise("dot com"), '.com ')

    def test_load(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._denormal_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "denormal.txt",
                                                                     format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.DENORMAL] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.DENORMAL] = storage_engine

        collection = DenormalCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertEqual(collection.denormalise_string(None, "keithsterling dot com"), "keithsterling.com")
        self.assertIsNone(collection.denormalise("dot cox"))

    def test_reload(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._denormal_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "denormal.txt",
                                                                     format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.DENORMAL] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.DENORMAL] = storage_engine

        collection = DenormalCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertEqual(collection.denormalise_string(None, "keithsterling dot com"), "keithsterling.com")
        self.assertIsNone(collection.denormalise("dot cox"))

        collection.reload(storage_factory)

        self.assertEqual(collection.denormalise_string(None, "keithsterling dot com"), "keithsterling.com")
        self.assertIsNone(collection.denormalise("dot cox"))

    def test_collection_operations_JP(self):
        collection = DenormalCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup("丸１", "①")
        tokenizer = TokenizerJP()

        self.assertTrue(collection.has_keyVal("丸１"))
        self.assertEqual("①", collection.value("丸１"))

        self.assertEqual(collection.denormalise_string(tokenizer, "丸１の回答"), "①の回答")
        self.assertIsNone(collection.denormalise("丸"))

    def test_collection_invalid_jp(self):
        collection = DenormalCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup("丸1", "①")

        self.assertFalse(collection.has_keyVal("丸"))
        self.assertIsNone(collection.value("丸"))

        tokenizer = TokenizerJP()
        self.assertIsNone(collection.denormalise("丸"))
        self.assertEqual(collection.denormalise_string(tokenizer, "丸の回答"), "丸の回答")

    def test_collection_duplicate_jp(self):
        collection = DenormalCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup("丸1", "①")
        collection.add_to_lookup("丸1", "②")

        self.assertEqual(collection.denormalise("丸1"), '①')

    def test_load_jp(self):
        storage_factory = StorageFactory()
        tokenizer = TokenizerJP()

        file_store_config = FileStorageConfiguration()
        file_store_config._denormal_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "denormal_jp.txt",
                                                                     format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.DENORMAL] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.DENORMAL] = storage_engine

        collection = DenormalCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertEqual(collection.denormalise_string(tokenizer, "丸1の回答"), "①の回答")
        self.assertIsNone(collection.denormalise("丸"))

    def test_reload_jp(self):
        storage_factory = StorageFactory()
        tokenizer = TokenizerJP()

        file_store_config = FileStorageConfiguration()
        file_store_config._denormal_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "denormal_jp.txt",
                                                                     format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.DENORMAL] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.DENORMAL] = storage_engine

        collection = DenormalCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertEqual(collection.denormalise_string(tokenizer, "丸1の回答"), "①の回答")
        self.assertIsNone(collection.denormalise("丸"))

        collection.reload(storage_factory)

        self.assertEqual(collection.denormalise_string(tokenizer, "丸1の回答"), "①の回答")
        self.assertIsNone(collection.denormalise("丸"))
