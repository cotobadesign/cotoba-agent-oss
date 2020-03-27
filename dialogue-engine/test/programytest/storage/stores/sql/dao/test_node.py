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

from programy.storage.stores.sql.dao.node import PatternNode
from programy.storage.stores.sql.dao.node import TemplateNode


class PatternNodeTests(unittest.TestCase):

    def test_init(self):
        node1 = PatternNode(name='name', node_class='class')
        self.assertIsNotNone(node1)
        self.assertEqual("<Pattern Node(id='n/a', name='name', node_class='class')>", str(node1))

        node2 = PatternNode(id=1, name='name', node_class='class')
        self.assertIsNotNone(node2)
        self.assertEqual("<Pattern Node(id='1', name='name', node_class='class')>", str(node2))


class TemplateNodeTests(unittest.TestCase):

    def test_init(self):
        node1 = TemplateNode(name='name', node_class='class')
        self.assertIsNotNone(node1)
        self.assertEqual("<Template Node(id='n/a', name='name', node_class='class')>", str(node1))

        node2 = TemplateNode(id=1, name='name', node_class='class')
        self.assertIsNotNone(node2)
        self.assertEqual("<Template Node(id='1', name='name', node_class='class')>", str(node2))
