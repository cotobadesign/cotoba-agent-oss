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

from programy.storage.stores.nosql.mongo.dao.corpus import Corpus


class CorpusTests(unittest.TestCase):

    def test_init_no_id(self):
        corpus = Corpus(words=["keiffster", "ABCDEF123", "PASSWORD123"])

        self.assertIsNotNone(corpus)
        self.assertIsNone(corpus.id)
        self.assertEqual(["keiffster", "ABCDEF123", "PASSWORD123"], corpus.words)

        self.assertEqual({'words': ['keiffster', 'ABCDEF123', 'PASSWORD123']}, corpus.to_document())

    def test_init_with_id(self):
        corpus = Corpus(words=["keiffster", "ABCDEF123", "PASSWORD123"])
        corpus.id = '666'

        self.assertIsNotNone(corpus)
        self.assertIsNotNone(corpus.id)
        self.assertEqual(["keiffster", "ABCDEF123", "PASSWORD123"], corpus.words)

        self.assertEqual({'_id': '666', 'words': ['keiffster', 'ABCDEF123', 'PASSWORD123']}, corpus.to_document())

    def test_from_document(self):
        corpus1 = Corpus.from_document({'words': ['keiffster', 'ABCDEF123', 'PASSWORD123']})
        self.assertIsNotNone(corpus1)
        self.assertIsNone(corpus1.id)
        self.assertEqual(['keiffster', 'ABCDEF123', 'PASSWORD123'], corpus1.words)

        corpus2 = Corpus.from_document({'_id': '666', 'words': ['keiffster', 'ABCDEF123', 'PASSWORD123']})
        self.assertIsNotNone(corpus2)
        self.assertEqual("666", corpus2.id)
        self.assertEqual(['keiffster', 'ABCDEF123', 'PASSWORD123'], corpus2.words)
