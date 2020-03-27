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
import os
import os.path
from time import sleep
from datetime import datetime

from programy.storage.stores.file.store.rdfs import FileRDFStore, FileRDFUpdatesStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.rdf.collection import RDFCollection
from programy.storage.stores.file.config import FileStoreConfiguration

from programytest.storage.asserts.store.assert_rdfs import RDFStoreAsserts


class FileRDFStoreTests(RDFStoreAsserts):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileRDFStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_load_from_test_dir_no_subdir(self):
        config = FileStorageConfiguration()
        config._rdf_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "rdfs" + os.sep + "text"],
                                                     extension="rdf", subdirs=False, format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileRDFStore(engine)

        map_collection = RDFCollection()
        store.load_all(map_collection)

        self.assertTrue(map_collection.contains('ACTIVITY'))

    def test_load_from_test_dir_with_subdir(self):
        config = FileStorageConfiguration()
        config._rdf_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "rdfs" + os.sep + "text"],
                                                     extension="rdf", subdirs=True, format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileRDFStore(engine)

        map_collection = RDFCollection()
        store.load_all(map_collection)

        self.assertTrue(map_collection.contains('ACTIVITY'))
        self.assertTrue(map_collection.contains('ANIMAL'))

    def test_rdf_add_entry(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "rdf_updates"
        config.rdf_updates_storage._dirs = [tmpdir]
        config.rdf_updates_storage._has_single_file = True

        engine = FileStorageEngine(config)
        engine.initialise()
        updates_store = FileRDFUpdatesStore(engine)
        filepath = updates_store._updates_filename(updates_store._get_storage_path())

        updates_store.empty_updates()
        self.assertFalse(os.path.exists(filepath))

        updates_store.add_entry("subject", "predicate", "object")

        self.assertTrue(os.path.exists(filepath))

        updates_store.empty_updates()
        self.assertFalse(os.path.exists(filepath))

    def test_apply_rdf_delete_entry(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "rdf_updates"
        config.rdf_updates_storage._dirs = [tmpdir]
        config.rdf_updates_storage._has_single_file = True

        engine = FileStorageEngine(config)
        engine.initialise()
        updates_store = FileRDFUpdatesStore(engine)
        filepath = updates_store._updates_filename(updates_store._get_storage_path())

        updates_store.empty_updates()
        self.assertFalse(os.path.exists(filepath))

        updates_store.delete_entry("subject1", "predicate", "object")
        updates_store.delete_entry("subject2", "predicate", None)
        updates_store.delete_entry("subject2", None, None)

        self.assertTrue(os.path.exists(filepath))

        updates_store.empty_updates()
        self.assertFalse(os.path.exists(filepath))

    def test_apply_rdf_updates(self):
        config = FileStorageConfiguration()
        config._rdf_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "rdfs" + os.sep + "text"],
                                                     extension="rdf", subdirs=True, format="text", encoding="utf-8", delete_on_start=False)
        tmpdir = os.path.dirname(__file__) + os.sep + "rdf_updates"
        config.rdf_updates_storage._dirs = [tmpdir]
        config.rdf_updates_storage._has_single_file = True

        engine = FileStorageEngine(config)
        engine.initialise()
        rdf_store = FileRDFStore(engine)
        updates_store = FileRDFUpdatesStore(engine)
        filepath = updates_store._updates_filename(updates_store._get_storage_path())

        updates_store.empty_updates()
        self.assertFalse(os.path.exists(filepath))

        updates_store.add_entry("subject1", "predicate1", "object1")
        updates_store.add_entry("subject2", "predicate2", "object2")
        updates_store.add_entry("subject3", "predicate3", "object3")
        updates_store.delete_entry("subject2", None, None)
        updates_store.delete_entry("subject3", "predicate3", None)

        map_collection = RDFCollection()
        rdf_store.load_all(map_collection)

        updates_store.apply_rdf_updates(map_collection, None)

        self.assertTrue(map_collection.has_subject('SUBJECT1'))
        self.assertFalse(map_collection.has_subject('SUBJECT2'))
        self.assertFalse(map_collection.has_subject('SUBJECT3'))

        updates_store.empty_updates()
        self.assertFalse(os.path.exists(filepath))

    def test_apply_rdf_updates_before(self):
        config = FileStorageConfiguration()
        config._rdf_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "rdfs" + os.sep + "text"],
                                                     extension="rdf", subdirs=True, format="text", encoding="utf-8", delete_on_start=False)
        tmpdir = os.path.dirname(__file__) + os.sep + "rdf_updates"
        config.rdf_updates_storage._dirs = [tmpdir]
        config.rdf_updates_storage._has_single_file = True

        engine = FileStorageEngine(config)
        engine.initialise()
        rdf_store = FileRDFStore(engine)
        updates_store = FileRDFUpdatesStore(engine)
        filepath = updates_store._updates_filename(updates_store._get_storage_path())

        updates_store.empty_updates()
        self.assertFalse(os.path.exists(filepath))

        updates_store.add_entry("subject1", "predicate1", "object1")
        updates_store.add_entry("subject2", "predicate2", "object2")
        updates_store.add_entry("subject3", "predicate3", "object3")
        updates_store.delete_entry("subject2", None, None)
        updates_store.delete_entry("subject3", "predicate3", None)

        sleep(1)

        map_collection = RDFCollection()
        rdf_store.load_all(map_collection)
        lastDate = datetime.now()

        updates_store.apply_rdf_updates(map_collection, lastDate)

        self.assertFalse(map_collection.has_subject('SUBJECT1'))
        self.assertFalse(map_collection.has_subject('SUBJECT2'))
        self.assertFalse(map_collection.has_subject('SUBJECT3'))

        updates_store.empty_updates()
        self.assertFalse(os.path.exists(filepath))

    def test_apply_rdf_updates_after(self):
        config = FileStorageConfiguration()
        config._rdf_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "rdfs" + os.sep + "text"],
                                                     extension="rdf", subdirs=True, format="text", encoding="utf-8", delete_on_start=False)
        tmpdir = os.path.dirname(__file__) + os.sep + "rdf_updates"
        config.rdf_updates_storage._dirs = [tmpdir]
        config.rdf_updates_storage._has_single_file = True

        engine = FileStorageEngine(config)
        engine.initialise()
        rdf_store = FileRDFStore(engine)
        updates_store = FileRDFUpdatesStore(engine)
        filepath = updates_store._updates_filename(updates_store._get_storage_path())

        updates_store.empty_updates()
        self.assertFalse(os.path.exists(filepath))

        map_collection = RDFCollection()
        rdf_store.load_all(map_collection)
        lastDate = datetime.now()

        sleep(1)

        updates_store.add_entry("subject1", "predicate1", "object1")
        updates_store.add_entry("subject2", "predicate2", "object2")
        updates_store.add_entry("subject3", "predicate3", "object3")
        updates_store.delete_entry("subject2", None, None)
        updates_store.delete_entry("subject3", "predicate3", None)

        updates_store.apply_rdf_updates(map_collection, lastDate)

        self.assertTrue(map_collection.has_subject('SUBJECT1'))
        self.assertFalse(map_collection.has_subject('SUBJECT2'))
        self.assertFalse(map_collection.has_subject('SUBJECT3'))

        updates_store.empty_updates()
        self.assertFalse(os.path.exists(filepath))

    def test_apply_rdf_updates_intime(self):
        config = FileStorageConfiguration()
        config._rdf_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "rdfs" + os.sep + "text"],
                                                     extension="rdf", subdirs=True, format="text", encoding="utf-8", delete_on_start=False)
        tmpdir = os.path.dirname(__file__) + os.sep + "rdf_updates"
        config.rdf_updates_storage._dirs = [tmpdir]
        config.rdf_updates_storage._has_single_file = True

        engine = FileStorageEngine(config)
        engine.initialise()
        rdf_store = FileRDFStore(engine)
        updates_store = FileRDFUpdatesStore(engine)
        filepath = updates_store._updates_filename(updates_store._get_storage_path())

        updates_store.empty_updates()
        self.assertFalse(os.path.exists(filepath))

        map_collection = RDFCollection()
        rdf_store.load_all(map_collection)

        updates_store.add_entry("subject1", "predicate1", "object1")
        updates_store.add_entry("subject2", "predicate2", "object2")

        lastDate = datetime.now()
        sleep(1)

        updates_store.add_entry("subject3", "predicate3", "object3")
        updates_store.delete_entry("subject2", None, None)

        updates_store.apply_rdf_updates(map_collection, lastDate)

        self.assertFalse(map_collection.has_subject('SUBJECT1'))
        self.assertFalse(map_collection.has_subject('SUBJECT2'))
        self.assertTrue(map_collection.has_subject('SUBJECT3'))

        updates_store.empty_updates()
        self.assertFalse(os.path.exists(filepath))

    def test_apply_rdf_updates_No_files(self):
        config = FileStorageConfiguration()
        config._rdf_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "rdfs" + os.sep + "text"],
                                                     extension="rdf", subdirs=True, format="text", encoding="utf-8", delete_on_start=False)
        tmpdir = os.path.dirname(__file__) + os.sep + "rdf_updates"
        config.rdf_updates_storage._dirs = [tmpdir]
        config.rdf_updates_storage._has_single_file = True

        engine = FileStorageEngine(config)
        engine.initialise()
        rdf_store = FileRDFStore(engine)
        updates_store = FileRDFUpdatesStore(engine)
        filepath = updates_store._updates_filename(updates_store._get_storage_path())

        updates_store.empty_updates()
        self.assertFalse(os.path.exists(filepath))

        map_collection = RDFCollection()
        rdf_store.load_all(map_collection)

        updates_store.apply_rdf_updates(map_collection, None)

        updates_store.empty_updates()
        self.assertFalse(os.path.exists(filepath))

    def test_save_rdf_data(self):
        config = FileStorageConfiguration()
        config._rdf_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "rdfs" + os.sep + "text"],
                                                     extension="rdf", subdirs=True, format="text", encoding="utf-8", delete_on_start=False)
        tmpdir = os.path.dirname(__file__) + os.sep + "rdf_updates"
        config.rdf_updates_storage._dirs = [tmpdir]
        config.rdf_updates_storage._has_single_file = True

        engine = FileStorageEngine(config)
        engine.initialise()
        rdf_store = FileRDFStore(engine)
        updates_store = FileRDFUpdatesStore(engine)
        filepath = updates_store._save_filename(updates_store._get_storage_path())

        updates_store.empty()
        self.assertFalse(os.path.exists(filepath))

        updates_store.save_rdf_data(None)
        self.assertFalse(os.path.exists(updates_store._get_storage_path()))

        map_collection = RDFCollection()
        rdf_store.load_all(map_collection)

        self.assertTrue(map_collection.contains('ACTIVITY'))
        self.assertTrue(map_collection.contains('ANIMAL'))

        updates_store.save_rdf_data(map_collection)
        self.assertTrue(os.path.exists(filepath))

        updates_store.empty()
        self.assertFalse(os.path.exists(filepath))

    def test_rdf_updates_other_case(self):
        config = FileStorageConfiguration()
        config._rdf_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "rdfs" + os.sep + "text"],
                                                     extension="rdf", subdirs=True, format="text", encoding="utf-8", delete_on_start=False)
        tmpdir = os.path.dirname(__file__) + os.sep + "rdf_updates"
        config.rdf_updates_storage._dirs = [tmpdir, tmpdir]
        config.rdf_updates_storage._has_single_file = True
        engine = FileStorageEngine(config)
        engine.initialise()
        updates_store = FileRDFUpdatesStore(engine)
        filepath = updates_store._updates_filename(updates_store._get_storage_path())

        updates_store.empty()
        self.assertFalse(os.path.exists(filepath))

        self.assertEqual(updates_store.get_storage(), config.rdf_updates_storage)
