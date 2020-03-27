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

from programy.storage.stores.nosql.mongo.dao.map import Map


class MapTests(unittest.TestCase):

    def test_init_no_id(self):
        amap = Map(name="TEST", key_values={"key1": "val1", "key2": "val2"})

        self.assertIsNotNone(amap)
        self.assertIsNone(amap.id)
        self.assertEqual("TEST", amap.name)
        self.assertEqual({"key1": "val1", "key2": "val2"}, amap.key_values)
        self.assertEqual({'key_values': {'key1': 'val1', 'key2': 'val2'}, 'name': 'TEST'}, amap.to_document())

    def test_init_with_id(self):
        amap = Map(name="TEST", key_values={"key1": "val1", "key2": "val2"})
        amap.id = '666'

        self.assertIsNotNone(amap)
        self.assertIsNotNone(amap.id)
        self.assertEqual('666', amap.id)
        self.assertEqual("TEST", amap.name)
        self.assertEqual({"key1": "val1", "key2": "val2"}, amap.key_values)
        self.assertEqual({'_id': '666', 'key_values': {'key1': 'val1', 'key2': 'val2'}, 'name': 'TEST'}, amap.to_document())

    def test_from_document(self):
        amap1 = Map.from_document({'key_values': {'key1': 'val1', 'key2': 'val2'}, 'name': 'TEST'})
        self.assertIsNotNone(amap1)
        self.assertIsNone(amap1.id)
        self.assertEqual("TEST", amap1.name)
        self.assertEqual({"key1": "val1", "key2": "val2"}, amap1.key_values)

        amap2 = Map.from_document({'_id': '666', 'key_values': {'key1': 'val1', 'key2': 'val2'}, 'name': 'TEST'})
        self.assertIsNotNone(amap2)
        self.assertIsNotNone(amap2.id)
        self.assertEqual('666', amap2.id)
        self.assertEqual("TEST", amap2.name)
        self.assertEqual({"key1": "val1", "key2": "val2"}, amap2.key_values)
