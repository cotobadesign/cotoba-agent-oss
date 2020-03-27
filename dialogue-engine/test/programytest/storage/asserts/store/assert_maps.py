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

from programy.mappings.maps import MapCollection
from programy.storage.entities.store import Store


class MockMapCollection(object):

    def __init__(self):
        self.maps = {}

    def empty(self):
        self.maps.clear()

    def remove(self, name):
        self.maps.pop(name, None)

    def add_map(self, map_name, the_map, store):
        self.maps[map_name] = the_map


class MapStoreAsserts(unittest.TestCase):

    def assert_map_storage(self, store):
        store.empty()

        store.add_to_map("TESTMAP1", "Key1", "Val1")
        store.add_to_map("TESTMAP1", "Key2", "Val2")
        store.add_to_map("TESTMAP1", "Key3", "Val3")
        store.add_to_map("TESTMAP2", "Key1", "Val1")
        store.commit()

        map_collection = MockMapCollection()
        store.load_all(map_collection)
        self.assertEqual(2, len(map_collection.maps.keys()))
        self.assertTrue("TESTMAP1" in map_collection.maps)
        self.assertTrue("Val1", map_collection.maps['TESTMAP1']['Key1'])
        self.assertTrue("Val2", map_collection.maps['TESTMAP1']['Key2'])
        self.assertTrue("Val3", map_collection.maps['TESTMAP1']['Key3'])
        self.assertTrue("TESTMAP2" in map_collection.maps)
        self.assertTrue("Val1", map_collection.maps['TESTMAP2']['Key1'])

        store.remove_from_map("TESTMAP1", "Key1")
        store.remove_from_map("TESTMAP2", "Key1")
        store.commit()

        map_collection = MockMapCollection()
        store.load_all(map_collection)
        self.assertEqual(1, len(map_collection.maps.keys()))
        self.assertTrue("TESTMAP1" in map_collection.maps)
        self.assertTrue("Val2", map_collection.maps['TESTMAP1']['Key2'])
        self.assertTrue("Val3", map_collection.maps['TESTMAP1']['Key3'])
        self.assertFalse("TESTMAP2" in map_collection.maps)

    def assert_upload_from_text(self, store):
        store.empty()

        store.upload_from_text('TESTMAP', """
        ant:6
        bat:2
        bear:4
        bee:6
        bird:2
        """)

        map_collection = MapCollection()
        store.load(map_collection, 'TESTMAP')

        self.assertTrue(map_collection.contains('TESTMAP'))
        map = map_collection.map('TESTMAP')
        self.assertIsNotNone(map)
        self.assertTrue('ANT' in map)
        self.assertEqual('6', map['ANT'])

    def assert_upload_text_files_from_directory_no_subdir(self, store):
        store.empty()

        store.upload_from_directory(os.path.dirname(__file__) + os.sep + "data" + os.sep + "maps" + os.sep + "text", subdir=False)

        map_collection = MapCollection()
        store.load(map_collection, 'TESTMAP')

        self.assertTrue(map_collection.contains('TESTMAP'))
        map = map_collection.map('TESTMAP')
        self.assertIsNotNone(map)
        self.assertTrue('ANT' in map)
        self.assertEqual('6', map['ANT'])

    def assert_upload_from_csv_file(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "maps" + os.sep + "csv" + os.sep + "testmap.csv", format=Store.CSV_FORMAT)

        map_collection = MapCollection()
        store.load(map_collection, 'TESTMAP')

        self.assertTrue(map_collection.contains('TESTMAP'))
        map = map_collection.map('TESTMAP')
        self.assertIsNotNone(map)
        self.assertTrue('ANT' in map)
        self.assertEqual('6', map['ANT'])

    def assert_upload_csv_files_from_directory_with_subdir(self, store):

        store.empty()

        store.upload_from_directory(os.path.dirname(__file__)+os.sep+"data"+os.sep+"maps"+os.sep+"csv", format=Store.CSV_FORMAT)

        map_collection = MapCollection()
        store.load_all(map_collection)

        self.assertTrue(map_collection.contains('TESTMAP'))
        map = map_collection.map('TESTMAP')
        self.assertIsNotNone(map)
        self.assertTrue('ANT' in map)
        self.assertEqual('6', map['ANT'])

        self.assertTrue(map_collection.contains('TESTMAP2'))
        self.assertEqual('sql', map_collection.storename('TESTMAP2'))
        map = map_collection.map('TESTMAP2')
        self.assertIsNotNone(map)
        self.assertTrue('BIRD' in map)
        self.assertEqual('fur', map['BIRD'])
