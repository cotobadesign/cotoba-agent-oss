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

from programy.storage.stores.nosql.mongo.dao.processor import PreProcessor
from programy.storage.stores.nosql.mongo.dao.processor import PostProcessor


class PreProcessorTests(unittest.TestCase):

    def test_init_no_id(self):
        processor = PreProcessor(classname="test.processorclass")

        self.assertIsNotNone(processor)
        self.assertIsNone(processor.id)
        self.assertEqual("test.processorclass", processor.classname)
        self.assertEqual({'classname': 'test.processorclass'}, processor.to_document())

    def test_init_with_id(self):
        processor = PreProcessor(classname="test.processorclass")
        processor.id = '666'

        self.assertIsNotNone(processor)
        self.assertIsNotNone(processor.id)
        self.assertEqual('666', processor.id)
        self.assertEqual("test.processorclass", processor.classname)
        self.assertEqual({'_id': '666', 'classname': 'test.processorclass'}, processor.to_document())

    def test_from_document(self):
        processor1 = PreProcessor.from_document({'classname': 'test.processorclass'})
        self.assertIsNotNone(processor1)
        self.assertIsNone(processor1.id)
        self.assertEqual("test.processorclass", processor1.classname)

        processor2 = PreProcessor.from_document({'_id': '666', 'classname': 'test.processorclass'})
        self.assertIsNotNone(processor2)
        self.assertIsNotNone(processor2.id)
        self.assertEqual('666', processor2.id)
        self.assertEqual("test.processorclass", processor2.classname)


class PostProcessorTests(unittest.TestCase):

    def test_init_no_id(self):
        processor = PostProcessor(classname="test.processorclass")

        self.assertIsNotNone(processor)
        self.assertIsNone(processor.id)
        self.assertEqual("test.processorclass", processor.classname)
        self.assertEqual({'classname': 'test.processorclass'}, processor.to_document())

    def test_init_with_id(self):
        processor = PostProcessor(classname="test.processorclass")
        processor.id = '666'

        self.assertIsNotNone(processor)
        self.assertIsNotNone(processor.id)
        self.assertEqual('666', processor.id)
        self.assertEqual("test.processorclass", processor.classname)
        self.assertEqual({'_id': '666', 'classname': 'test.processorclass'}, processor.to_document())

    def test_from_document(self):
        processor1 = PostProcessor.from_document({'classname': 'test.processorclass'})
        self.assertIsNotNone(processor1)
        self.assertIsNone(processor1.id)
        self.assertEqual("test.processorclass", processor1.classname)

        processor2 = PostProcessor.from_document({'_id': '666', 'classname': 'test.processorclass'})
        self.assertIsNotNone(processor2)
        self.assertIsNotNone(processor2.id)
        self.assertEqual('666', processor2.id)
        self.assertEqual("test.processorclass", processor2.classname)
