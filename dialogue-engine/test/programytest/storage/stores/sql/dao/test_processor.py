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

from programy.storage.stores.sql.dao.processor import PreProcessor
from programy.storage.stores.sql.dao.processor import PostProcessor


class PreProcessorTests(unittest.TestCase):

    def test_init(self):
        processor1 = PreProcessor(classname='class')
        self.assertIsNotNone(processor1)
        self.assertEqual("<PreProcessor Node(id='n/a', classname='class')>", str(processor1))

        processor2 = PreProcessor(id=1, classname='class')
        self.assertIsNotNone(processor2)
        self.assertEqual("<PreProcessor Node(id='1', classname='class')>", str(processor2))


class PostProcessorTests(unittest.TestCase):

    def test_init(self):
        processor1 = PostProcessor(classname='class')
        self.assertIsNotNone(processor1)
        self.assertEqual("<PostProcessor Node(id='n/a', classname='class')>", str(processor1))

        processor2 = PostProcessor(id=1, classname='class')
        self.assertIsNotNone(processor2)
        self.assertEqual("<PostProcessor Node(id='1', classname='class')>", str(processor2))
