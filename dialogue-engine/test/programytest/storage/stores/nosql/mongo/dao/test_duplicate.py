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

from programy.storage.stores.nosql.mongo.dao.duplicate import Duplicate


class DuplicateTests(unittest.TestCase):

    def test_init_no_id(self):
        duplicate = Duplicate(duplicate="This is a duplicate", file='afile', start='300', end='500')

        self.assertIsNotNone(duplicate)
        self.assertIsNone(duplicate.id)
        self.assertEqual('This is a duplicate', duplicate.duplicate)
        self.assertEqual('afile', duplicate.file)
        self.assertEqual('300', duplicate.start)
        self.assertEqual('500', duplicate.end)
        self.assertEqual({'duplicate': 'This is a duplicate', 'end': '500', 'file': 'afile', 'start': '300'}, duplicate.to_document())

    def test_init_with_id(self):
        duplicate = Duplicate(duplicate="This is a duplicate", file='afile', start='300', end='500')
        duplicate.id = '666'

        self.assertIsNotNone(duplicate)
        self.assertIsNotNone(duplicate.id)
        self.assertEqual('666', duplicate.id)
        self.assertEqual('This is a duplicate', duplicate.duplicate)
        self.assertEqual('afile', duplicate.file)
        self.assertEqual('300', duplicate.start)
        self.assertEqual('500', duplicate.end)
        self.assertEqual({'_id': '666', 'duplicate': 'This is a duplicate', 'end': '500', 'file': 'afile', 'start': '300'}, duplicate.to_document())

    def test_from_document(self):
        duplicate1 = Duplicate.from_document({'duplicate': 'This is a duplicate', 'end': '500', 'file': 'afile', 'start': '300'})
        self.assertIsNotNone(duplicate1)
        self.assertIsNone(duplicate1.id)
        self.assertEqual('This is a duplicate', duplicate1.duplicate)
        self.assertEqual('afile', duplicate1.file)
        self.assertEqual('300', duplicate1.start)
        self.assertEqual('500', duplicate1.end)

        duplicate2 = Duplicate.from_document({'_id': '666', 'duplicate': 'This is a duplicate', 'end': '500', 'file': 'afile', 'start': '300'})
        self.assertIsNotNone(duplicate2)
        self.assertIsNotNone(duplicate2.id)
        self.assertEqual('666', duplicate2.id)
        self.assertEqual('This is a duplicate', duplicate1.duplicate)
        self.assertEqual('afile', duplicate1.file)
        self.assertEqual('300', duplicate1.start)
        self.assertEqual('500', duplicate1.end)
