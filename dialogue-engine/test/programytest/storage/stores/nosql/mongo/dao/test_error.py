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

from programy.storage.stores.nosql.mongo.dao.error import Error


class ErrorTests(unittest.TestCase):

    def test_init_no_id(self):
        error = Error(error="This is a error", file='afile', start='300', end='500')

        self.assertIsNotNone(error)
        self.assertIsNone(error.id)
        self.assertEqual('This is a error', error.error)
        self.assertEqual('afile', error.file)
        self.assertEqual('300', error.start)
        self.assertEqual('500', error.end)
        self.assertEqual({'error': 'This is a error', 'end': '500', 'file': 'afile', 'start': '300'}, error.to_document())

    def test_init_with_id(self):
        error = Error(error="This is a error", file='afile', start='300', end='500')
        error.id = '666'

        self.assertIsNotNone(error)
        self.assertIsNotNone(error.id)
        self.assertEqual('666', error.id)
        self.assertEqual('This is a error', error.error)
        self.assertEqual('afile', error.file)
        self.assertEqual('300', error.start)
        self.assertEqual('500', error.end)
        self.assertEqual({'_id': '666', 'error': 'This is a error', 'end': '500', 'file': 'afile', 'start': '300'}, error.to_document())

    def test_from_document(self):
        error1 = Error.from_document({'error': 'This is a error', 'end': '500', 'file': 'afile', 'start': '300'})
        self.assertIsNotNone(error1)
        self.assertIsNone(error1.id)
        self.assertEqual('This is a error', error1.error)
        self.assertEqual('afile', error1.file)
        self.assertEqual('300', error1.start)
        self.assertEqual('500', error1.end)

        error2 = Error.from_document({'_id': '666', 'error': 'This is a error', 'end': '500', 'file': 'afile', 'start': '300'})
        self.assertIsNotNone(error2)
        self.assertIsNotNone(error2.id)
        self.assertEqual('666', error2.id)
        self.assertEqual('This is a error', error1.error)
        self.assertEqual('afile', error1.file)
        self.assertEqual('300', error1.start)
        self.assertEqual('500', error1.end)
