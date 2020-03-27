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

from programy.storage.stores.nosql.mongo.dao.license import LicenseKey


class LicenseKeyTests(unittest.TestCase):

    def test_init_no_id(self):
        license = LicenseKey(name='name', key='key')

        self.assertIsNotNone(license)
        self.assertIsNone(license.id)
        self.assertEqual('name', license.name)
        self.assertEqual('key', license.key)
        self.assertEqual({'key': 'key', 'name': 'name'}, license.to_document())

    def test_init_with_id(self):
        license = LicenseKey(name='name', key='key')
        license.id = '666'

        self.assertIsNotNone(license)
        self.assertIsNotNone(license.id)
        self.assertEqual('666', license.id)
        self.assertEqual('name', license.name)
        self.assertEqual('key', license.key)
        self.assertEqual({'_id': '666', 'key': 'key', 'name': 'name'}, license.to_document())

    def test_from_document(self):
        license1 = LicenseKey.from_document({'key': 'key', 'name': 'name'})
        self.assertIsNotNone(license1)
        self.assertIsNone(license1.id)
        self.assertEqual('name', license1.name)
        self.assertEqual('key', license1.key)

        license2 = LicenseKey.from_document({'_id': '666', 'key': 'key', 'name': 'name'})
        self.assertIsNotNone(license2)
        self.assertIsNotNone(license2.id)
        self.assertEqual('666', license2.id)
        self.assertEqual('666', license2.id)
        self.assertEqual('name', license2.name)
        self.assertEqual('key', license2.key)
