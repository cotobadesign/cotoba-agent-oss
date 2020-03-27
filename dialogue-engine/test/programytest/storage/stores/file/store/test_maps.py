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
from programytest.storage.asserts.store.assert_maps import MapStoreAsserts
import os
import os.path

from programy.storage.stores.file.store.maps import FileMapsStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.mappings.maps import MapCollection
from programy.storage.stores.file.config import FileStoreConfiguration


class FileMapsStoreTests(MapStoreAsserts):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileMapsStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_load_from_test_dir_no_subdir(self):
        config = FileStorageConfiguration()
        config._maps_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "maps" + os.sep + "text"],
                                                      extension="txt", subdirs=False, format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileMapsStore(engine)

        map_collection = MapCollection()
        store.load_all(map_collection)

        self.assertTrue(map_collection.contains('TESTMAP'))
        the_map = map_collection.map('TESTMAP')
        self.assertIsNotNone(the_map)
        self.assertEqual("6", the_map['ANT'])

    def test_load_from_test_dir_with_subdir(self):
        config = FileStorageConfiguration()
        config._maps_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "maps" + os.sep + "text"],
                                                      extension="txt", subdirs=True, format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileMapsStore(engine)

        map_collection = MapCollection()
        store.load_all(map_collection)

        self.assertTrue(map_collection.contains('TESTMAP'))
        the_map = map_collection.map('TESTMAP')
        self.assertIsNotNone(the_map)
        self.assertEqual("6", the_map['ANT'])

        self.assertTrue(map_collection.contains('TESTMAP2'))
        the_map = map_collection.map('TESTMAP2')
        self.assertIsNotNone(the_map)
        self.assertEqual("grrrrr", the_map['BEAR'])

    def test_load_single_file(self):
        config = FileStorageConfiguration()
        config._maps_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "data" + os.sep + "maps" + os.sep + "text" + os.sep + "testmap.txt"],
                                                      extension="txt", subdirs=True, format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileMapsStore(engine)

        map_collection = MapCollection()
        store.load(map_collection)

        self.assertTrue(map_collection.contains('TESTMAP'))
        the_map = map_collection.map('TESTMAP')
        self.assertIsNotNone(the_map)
        self.assertEqual("6", the_map['ANT'])
