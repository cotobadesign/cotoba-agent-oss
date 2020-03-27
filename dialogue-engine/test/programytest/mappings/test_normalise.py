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
from programy.mappings.normal import NormalCollection
from programy.storage.factory import StorageFactory
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStoreConfiguration


class NormaliseTests(unittest.TestCase):

    def test_initialise_collection(self):
        collection = NormalCollection()
        self.assertIsNotNone(collection)

    def test_collection_replace_string(self):
        normal_text = """
        ".ac ","dot ac"
        ".au","dot au"
        ".ca","dot ca"
        ".ch","dot ch"
        ".com","dot com"
        ".co","dot co"
        """

        collection = NormalCollection()
        self.assertIsNotNone(collection)

        collection.load_from_text(normal_text)

        self.assertTrue(collection.has_replace_key(".com"))
        self.assertEqual('dot com', collection.replace_value(".com"))

        self.assertEqual("keithsterling dot com", collection.normalise_string(None, "keithsterling.com"))

    def test_collection_string_invalid(self):
        collection = NormalCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup(".com", 'dot com')

        self.assertFalse(collection.has_replace_key(".cox"))
        self.assertIsNone(collection.replace_value(".cox"))

        self.assertIsNone(collection.normalise(".cox"))
        self.assertEqual("keithsterling dot com", collection.normalise_string(None, "keithsterling.com"))

    def test_collection_string_duplicate(self):
        collection = NormalCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup(".com", 'dot com')
        collection.add_to_lookup(".com", "dot co")

        self.assertEqual("keithsterling dot com", collection.normalise_string(None, "keithsterling.com"))

    def test_collection_replace_words(self):
        normal_text = """
        " couldn't","could not"
        " didn't","did not"
        " doesn't","does not"
        " don't","do not"
        " down load","download"
        """

        collection = NormalCollection()
        self.assertIsNotNone(collection)

        collection.load_from_text(normal_text)

        self.assertTrue(collection.has_keyVal("down load"))
        self.assertEqual('download', collection.value("down load"))

        self.assertEqual('download', collection.normalise("down load"))
        self.assertEqual("gip file download", collection.normalise_string(None, "gip file down load"))

    def test_collection_words_invalid(self):
        collection = NormalCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup(" do not", "do not")

        self.assertFalse(collection.has_keyVal("dont"))
        self.assertIsNone(collection.value("dont"))

        self.assertIsNone(collection.normalise("dont"))
        self.assertEqual("he do nt it", collection.normalise_string(None, "he do nt it"))

    def test_collection_words_duplicate(self):
        collection = NormalCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup(" don't", "do not")
        collection.add_to_lookup(" don't", "donot")

        self.assertEqual("he do not it", collection.normalise_string(None, "he don't it"))

    def test_load(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._normal_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "normal.txt",
                                                                   format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.NORMAL] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.NORMAL] = storage_engine

        collection = NormalCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertEqual(collection.normalise_string(None, "keithsterling.com"), "keithsterling dot com")

    def test_reload(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._normal_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "normal.txt",
                                                                   format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.NORMAL] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.NORMAL] = storage_engine

        collection = NormalCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertEqual(collection.normalise_string(None, "keithsterling.com"), "keithsterling dot com")

        collection.reload(storage_factory)

        self.assertEqual(collection.normalise_string(None, "keithsterling.com"), "keithsterling dot com")

    def test_collection_operations_JP(self):
        collection = NormalCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup("①", '丸１')
        tokenizer = TokenizerJP()

        self.assertTrue(collection.has_keyVal("①"))
        self.assertEqual('丸１', collection.value("①"))

        self.assertEqual("丸１の回答", collection.normalise_string(tokenizer, "①の回答"))

    def test_collection_invalid_jp(self):
        collection = NormalCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup("彼岸", 'お彼岸')

        self.assertFalse(collection.has_keyVal("彼氏"))
        self.assertIsNone(collection.value("彼氏"))

        tokenizer = TokenizerJP()
        self.assertIsNone(collection.normalise("彼氏"))
        self.assertEqual("彼氏の回答", collection.normalise_string(tokenizer, "彼氏の回答"))

    def test_collection_duplicate_jp(self):
        collection = NormalCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup("①", '丸1')
        collection.add_to_lookup("①", '丸2')

        tokenizer = TokenizerJP()
        self.assertEqual("丸1の回答", collection.normalise_string(tokenizer, "①の回答"))

    def test_load_jp(self):
        storage_factory = StorageFactory()
        tokenizer = TokenizerJP()

        file_store_config = FileStorageConfiguration()
        file_store_config._normal_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "normal_jp.txt",
                                                                   format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.NORMAL] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.NORMAL] = storage_engine

        collection = NormalCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertEqual("丸1の回答", collection.normalise_string(tokenizer, "①の回答"))

    def test_reload_jp(self):
        storage_factory = StorageFactory()
        tokenizer = TokenizerJP()

        file_store_config = FileStorageConfiguration()
        file_store_config._normal_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "normal_jp.txt",
                                                                   format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.NORMAL] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.NORMAL] = storage_engine

        collection = NormalCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertEqual("丸1の回答", collection.normalise_string(tokenizer, "①の回答"))

        collection.reload(storage_factory)

        self.assertEqual("丸1の回答", collection.normalise_string(tokenizer, "①の回答"))
