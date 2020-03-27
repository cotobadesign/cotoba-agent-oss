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
import os.path

from programy.rdf.collection import RDFCollection
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.factory import StorageFactory


class RDFCollectionLoadingTests(unittest.TestCase):

    def test_load_from_file(self):
        config = FileStorageConfiguration()
        config._rdf_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "rdfs"])

        factory = StorageFactory()

        storage_engine = FileStorageEngine(config)

        factory._storage_engines[StorageFactory.RDF] = storage_engine
        factory._store_to_engine_map[StorageFactory.RDF] = storage_engine

        storage_engine.initialise()

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.load(factory)

        self.assertTrue(collection.has_subject("TEST1"))
        self.assertTrue(collection.has_predicate("TEST1", "HASPURPOSE"))
        self.assertTrue(collection.has_object("TEST1", "HASPURPOSE", "to test"))

    def test_reload_from_file(self):
        config = FileStorageConfiguration()
        config._rdf_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "rdfs"])

        factory = StorageFactory()

        storage_engine = FileStorageEngine(config)

        factory._storage_engines[StorageFactory.RDF] = storage_engine
        factory._store_to_engine_map[StorageFactory.RDF] = storage_engine

        storage_engine.initialise()

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.load(factory)

        self.assertTrue(collection.has_subject("TEST1"))
        self.assertTrue(collection.has_predicate("TEST1", "HASPURPOSE"))
        self.assertTrue(collection.has_object("TEST1", "HASPURPOSE", "to test"))

        collection.delete_entity("TEST1", "HASPURPOSE", "to test")
        self.assertFalse(collection.has_object("TEST1", "HASPURPOSE", "to test"))

        collection.reload(factory, "TESTDATA")

        self.assertTrue(collection.has_subject("TEST1"))
        self.assertTrue(collection.has_predicate("TEST1", "HASPURPOSE"))
        self.assertTrue(collection.has_object("TEST1", "HASPURPOSE", "to test"))

    def test_save_to_file(self):
        config = FileStorageConfiguration()
        config._rdf_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "rdfs"])
        tmpdir = os.path.dirname(__file__) + os.sep + "rdf_updates"
        filepath = tmpdir + os.sep + "rdf_data.txt"
        config.rdf_updates_storage._dirs = [tmpdir]
        config.rdf_updates_storage._has_single_file = True

        factory = StorageFactory()

        storage_engine = FileStorageEngine(config)
        factory._storage_engines[StorageFactory.RDF] = storage_engine
        factory._store_to_engine_map[StorageFactory.RDF] = storage_engine
        factory._storage_engines[StorageFactory.RDF_UPDATES] = storage_engine
        factory._store_to_engine_map[StorageFactory.RDF_UPDATES] = storage_engine

        storage_engine.initialise()
        updates_engine = factory.entity_storage_engine(StorageFactory.RDF_UPDATES)
        updates_store = updates_engine.rdf_updates_store()
        updates_store.empty()

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.save_rdf_data()
        self.assertFalse(os.path.exists(filepath))

        collection.load(factory)

        self.assertTrue(collection.has_subject("TEST1"))
        self.assertTrue(collection.has_predicate("TEST1", "HASPURPOSE"))
        self.assertTrue(collection.has_object("TEST1", "HASPURPOSE", "to test"))

        collection.save_rdf_data()
        self.assertTrue(os.path.exists(filepath))

        updates_store.empty()
        self.assertFalse(os.path.exists(filepath))

    def test_apply_updates(self):
        config = FileStorageConfiguration()
        config._rdf_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "rdfs"])
        tmpdir = os.path.dirname(__file__) + os.sep + "rdf_updates"
        config.rdf_updates_storage._dirs = [tmpdir]
        config.rdf_updates_storage._has_single_file = True

        factory = StorageFactory()

        storage_engine = FileStorageEngine(config)
        factory._storage_engines[StorageFactory.RDF] = storage_engine
        factory._store_to_engine_map[StorageFactory.RDF] = storage_engine
        factory._storage_engines[StorageFactory.RDF_UPDATES] = storage_engine
        factory._store_to_engine_map[StorageFactory.RDF_UPDATES] = storage_engine

        storage_engine.initialise()
        updates_engine = factory.entity_storage_engine(StorageFactory.RDF_UPDATES)
        updates_store = updates_engine.rdf_updates_store()
        updates_store.empty()

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.load(factory)

        self.assertTrue(collection.has_subject("TEST1"))
        self.assertTrue(collection.has_predicate("TEST1", "HASPURPOSE"))
        self.assertTrue(collection.has_object("TEST1", "HASPURPOSE", "to test"))

        collection.apply_updates()
