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

from programy.storage.stores.nosql.mongo.dao.set import Set


class SetTests(unittest.TestCase):

    def test_init_no_id(self):
        aset = Set(name="TEST", values=["val1", "val2", "val3"])

        self.assertIsNotNone(aset)
        self.assertIsNone(aset.id)
        self.assertEqual("TEST", aset.name)
        self.assertEqual(["val1", "val2", "val3"], aset.values)
        self.assertEqual({'values': ["val1", "val2", "val3"], 'name': 'TEST'}, aset.to_document())

    def test_init_with_id(self):
        aset = Set(name="TEST", values=["val1", "val2", "val3"])
        aset.id = '666'

        self.assertIsNotNone(aset)
        self.assertIsNotNone(aset.id)
        self.assertEqual('666', aset.id)
        self.assertEqual("TEST", aset.name)
        self.assertEqual(["val1", "val2", "val3"], aset.values)
        self.assertEqual({'_id': '666', 'values': ["val1", "val2", "val3"], 'name': 'TEST'}, aset.to_document())

    def test_from_document(self):
        aset1 = Set.from_document({'values': ["val1", "val2", "val3"], 'name': 'TEST'})
        self.assertIsNotNone(aset1)
        self.assertIsNone(aset1.id)
        self.assertEqual("TEST", aset1.name)
        self.assertEqual(["val1", "val2", "val3"], aset1.values)

        aset2 = Set.from_document({'_id': '666', 'values': ["val1", "val2", "val3"], 'name': 'TEST'})
        self.assertIsNotNone(aset2)
        self.assertIsNotNone(aset2.id)
        self.assertEqual('666', aset2.id)
        self.assertEqual("TEST", aset2.name)
        self.assertEqual(["val1", "val2", "val3"], aset2.values)
