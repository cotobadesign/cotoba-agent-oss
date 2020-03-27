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
from programy.mappings.person import PersonCollection
from programy.storage.factory import StorageFactory
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStoreConfiguration


class PersonTests(unittest.TestCase):

    def test_initialise_collection(self):
        collection = PersonCollection()
        self.assertIsNotNone(collection)

    def test_collection_operations(self):
        person_text = """
        "with you","with me2"
        "with me","with you2"
        "are you","am I2"
        "with me","with you2"
        """

        collection = PersonCollection()
        self.assertIsNotNone(collection)

        collection.load_from_text(person_text)

        self.assertEqual(collection.personalise_string(None, "with me"), "with you2")
        self.assertEqual(collection.personalise_string(None, "Hello are you with me"), "Hello am I2 with you2")

        pattern = collection.person("WITH YOU")
        self.assertIsNotNone(pattern)
        self.assertEqual("with me2", pattern)

    def test_collection_invalid(self):
        collection = PersonCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup("with you", "with me")

        self.assertFalse(collection.has_keyVal("WITH HIM"))
        self.assertIsNone(collection.value("WITH HIM"))

        self.assertIsNone(collection.person("WITH HIM"))
        self.assertEqual(collection.personalise_string(None, "This is with him"), "This is with him")

    def test_collection_duplicate(self):
        collection = PersonCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup("with you", "with me")
        collection.add_to_lookup("with you", 'with him')

        self.assertEqual(collection.person("WITH YOU"), 'with me')

    def test_load(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._person_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "person.txt",
                                                                   format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.PERSON] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.PERSON] = storage_engine

        collection = PersonCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertEqual(collection.personalise_string(None, "with me"), "with you2")
        self.assertEqual(collection.personalise_string(None, "Hello are you with me"), "Hello am I2 with you2")

    def test_reload(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._person_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "person.txt",
                                                                   format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.PERSON] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.PERSON] = storage_engine

        collection = PersonCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertEqual(collection.personalise_string(None, "with me"), "with you2")
        self.assertEqual(collection.personalise_string(None, "Hello are you with me"), "Hello am I2 with you2")

        collection.reload(storage_factory)

        self.assertEqual(collection.personalise_string(None, "with me"), "with you2")
        self.assertEqual(collection.personalise_string(None, "Hello are you with me"), "Hello am I2 with you2")

    def test_collection_operations_jp(self):
        person_text = """
        "貴方","私"
        "私","貴方"
        "あなた","わたし"
        "わたし","あなた"
        """

        collection = PersonCollection()
        self.assertIsNotNone(collection)

        collection.load_from_text(person_text)
        tokenizer = TokenizerJP()

        self.assertEqual(collection.personalise_string(tokenizer, "私が正しい"), "貴方が正しい")
        self.assertEqual(collection.personalise_string(tokenizer, "あなたは変"), "わたしは変")

        pattern = collection.person("貴方")
        self.assertIsNotNone(pattern)
        self.assertEqual("私", pattern)

    def test_collection_invalid_JP(self):
        collection = PersonCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup("貴方", "私")

        self.assertFalse(collection.has_keyVal("彼"))
        self.assertIsNone(collection.value("彼"))

        tokenizer = TokenizerJP()
        self.assertIsNone(collection.person("彼"))
        self.assertEqual(collection.personalise_string(tokenizer, "彼が来た"), "彼が来た")

    def test_collection_duplicate_jp(self):
        collection = PersonCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup("貴方", "私")
        collection.add_to_lookup("貴方", '彼氏')

        self.assertEqual(collection.person("貴方"), '私')

    def test_load_jp(self):
        storage_factory = StorageFactory()
        tokenizer = TokenizerJP()

        file_store_config = FileStorageConfiguration()
        file_store_config._person_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "person_jp.txt",
                                                                   format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.PERSON] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.PERSON] = storage_engine

        collection = PersonCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertEqual(collection.personalise_string(tokenizer, "私が正しい"), "貴方が正しい")
        self.assertEqual(collection.personalise_string(tokenizer, "あなたは変"), "わたしは変")

    def test_reload_jp(self):
        storage_factory = StorageFactory()
        tokenizer = TokenizerJP()

        file_store_config = FileStorageConfiguration()
        file_store_config._person_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "person_jp.txt",
                                                                   format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.PERSON] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.PERSON] = storage_engine

        collection = PersonCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertEqual(collection.personalise_string(tokenizer, "私が正しい"), "貴方が正しい")
        self.assertEqual(collection.personalise_string(tokenizer, "あなたは変"), "わたしは変")

        collection.reload(storage_factory)

        self.assertEqual(collection.personalise_string(tokenizer, "私が正しい"), "貴方が正しい")
        self.assertEqual(collection.personalise_string(tokenizer, "あなたは変"), "わたしは変")
