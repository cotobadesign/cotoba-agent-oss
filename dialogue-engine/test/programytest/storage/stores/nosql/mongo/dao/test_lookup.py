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

from programy.storage.stores.nosql.mongo.dao.lookup import Lookup


class LookupTests(unittest.TestCase):

    def test_init_no_id(self):
        lookup = Lookup(key='key1', value='value1')

        self.assertIsNotNone(lookup)
        self.assertIsNone(lookup.id)
        self.assertEqual('key1', lookup.key)
        self.assertEqual('value1', lookup.value)
        self.assertEqual({'key': 'key1', 'value': 'value1'}, lookup.to_document())

    def test_init_with_id(self):
        lookup = Lookup(key='key1', value='value1')
        lookup.id = '666'

        self.assertIsNotNone(lookup)
        self.assertIsNotNone(lookup.id)
        self.assertEqual('666', lookup.id)
        self.assertEqual('key1', lookup.key)
        self.assertEqual('value1', lookup.value)
        self.assertEqual({'_id': '666', 'key': 'key1', 'value': 'value1'}, lookup.to_document())

    def test_from_document(self):
        lookup1 = Lookup.from_document({'key': 'key1', 'value': 'value1'})
        self.assertIsNotNone(lookup1)
        self.assertIsNone(lookup1.id)
        self.assertEqual('key1', lookup1.key)
        self.assertEqual('value1', lookup1.value)

        lookup2 = Lookup.from_document({'_id': '666', 'key': 'key1', 'value': 'value1'})
        self.assertIsNotNone(lookup2)
        self.assertIsNotNone(lookup2.id)
        self.assertEqual('666', lookup2.id)
        self.assertEqual('key1', lookup2.key)
        self.assertEqual('value1', lookup2.value)
