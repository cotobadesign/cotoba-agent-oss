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
from programytest.storage.asserts.store.assert_sets import SetStoreAsserts
import os

from programy.storage.stores.file.store.sets import FileSetsStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.mappings.sets import SetCollection
from programy.storage.stores.file.config import FileStoreConfiguration


class FileSetsStoreTests(SetStoreAsserts):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileSetsStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_load_from_test_dir_no_subdir(self):
        config = FileStorageConfiguration()
        config._sets_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "sets" + os.sep + "text"],
                                                      extension="txt", subdirs=False, format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileSetsStore(engine)

        set_collection = SetCollection()
        store.load_all(set_collection)

        self.assertTrue(set_collection.contains('TESTSET'))
        values = set_collection.set_list('TESTSET')
        self.assertTrue('VAL1' in values)
        self.assertTrue('VAL2' in values)
        self.assertTrue('VAL3' in values)
        self.assertTrue('VAL4' in values)

    def test_load_from_test_dir_with_subdir(self):
        config = FileStorageConfiguration()
        config._sets_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "sets" + os.sep + "text"],
                                                      extension="txt", subdirs=True, format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileSetsStore(engine)

        set_collection = SetCollection()
        store.load_all(set_collection)

        self.assertTrue(set_collection.contains('TESTSET'))
        values = set_collection.set_list('TESTSET')
        self.assertTrue('VAL1' in values)
        self.assertTrue('VAL2' in values)
        self.assertTrue('VAL3' in values)
        self.assertTrue('VAL4' in values)

        self.assertTrue(set_collection.contains('TESTSET2'))
        values = set_collection.set_list('TESTSET2')
        self.assertEqual(4, len(values))
        self.assertTrue('VAL5' in values)
        self.assertTrue('VAL6' in values)
        self.assertTrue('VAL7' in values)
        self.assertTrue('VAL8' in values)

    def test_load_single_file(self):
        config = FileStorageConfiguration()
        config._sets_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "sets" + os.sep + "text" + os.sep + "testset.txt"],
                                                      extension="txt", format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileSetsStore(engine)

        set_collection = SetCollection()
        store.load(set_collection)

        self.assertTrue(set_collection.contains('TESTSET'))
        values = set_collection.set_list('TESTSET')
        self.assertTrue('VAL1' in values)
        self.assertTrue('VAL2' in values)
        self.assertTrue('VAL3' in values)
        self.assertTrue('VAL4' in values)
