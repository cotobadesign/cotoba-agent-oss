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

from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.factory import StorageFactory
from programy.rdf.collection import RDFCollection


class RDFCollectionCreationTests(unittest.TestCase):

    def test_add_collection(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANIKING")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

    def test_add_multi_object_collection(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACTOR", "ISA", "PERSON", "TEST")
        collection.add_entity("ACTOR", "ISA", "MAN", "TEST")

        self.assertTrue(collection.has_subject('ACTOR'))

        self.assertTrue(collection.has_predicate('ACTOR', 'ISA'))

        self.assertTrue(collection.has_object('ACTOR', 'ISA', "PERSON"))
        self.assertTrue(collection.has_object('ACTOR', 'ISA', "MAN"))

    def test_delete_collection_subject(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANIKING")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_entity("ACCOUNT")

        self.assertFalse(collection.has_subject('ACCOUNT'))

    def test_delete_collection_subject_predicate(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANIKING")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_entity("ACCOUNT", "hasSize")

        self.assertFalse(collection.has_subject('ACCOUNT'))

    def test_delete_collection_subject_predicate_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANIKING")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_entity("ACCOUNT", "hasSize", "0")

        self.assertFalse(collection.has_subject('ACCOUNT'))
        self.assertFalse(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertFalse(collection.has_object('ACCOUNT', 'hasSize', "0"))

    def test_delete_collection_subject_predicate_diff_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANKING", "BANIKING")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_entity("ACCOUNT", "hasSize", "1")

        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

    def test_delete_collection_diff_subject(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANKING", "BANIKING")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_entity("ACCOUNT1", "hasSize", "0")

        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

    def test_delete_collection_diff_predicate(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANKING", "BANIKING")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_entity("ACCOUNT", "hasSize1", "1")

        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

    def test_delete_collection_diff_predicate_none_obj(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANKING", "BANIKING")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_entity("ACCOUNT", "hasSize1", None)

        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

    def test_collection_update_to_updates_file(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "rdf_updates"
        config.rdf_updates_storage._dirs = [tmpdir]
        config.rdf_updates_storage._has_single_file = True

        factory = StorageFactory()

        storage_engine = FileStorageEngine(config)
        factory._storage_engines[StorageFactory.RDF_UPDATES] = storage_engine
        factory._store_to_engine_map[StorageFactory.RDF_UPDATES] = storage_engine

        updates_engine = factory.entity_storage_engine(StorageFactory.RDF_UPDATES)
        updates_store = updates_engine.rdf_updates_store()
        updates_store.empty()

        collection = RDFCollection()
        self.assertIsNotNone(collection)
        collection._storage_factory = factory

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANKING", "BANIKING")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_entity("ACCOUNT", "hasSize", "0")

        self.assertFalse(collection.has_subject('ACCOUNT'))

        updates_store.empty()

    def test_collection_others(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANKING", "BANIKING")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        self.assertIsNone(collection.storename("BANKING1"))
        self.assertEqual(0, len(collection.predicates("account1")))
        self.assertEqual(0, len(collection.objects("ACCOUNT1", "hasSize")))
        self.assertEqual(0, len(collection.objects("ACCOUNT", "hasSize1")))
        self.assertFalse(collection.has_object("ACCOUNT", "hasSize", "1"))
