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

from programy.storage.stores.nosql.mongo.dao.node import PatternNode
from programy.storage.stores.nosql.mongo.dao.node import TemplateNode


class PatternNodeTests(unittest.TestCase):

    def test_init_no_id(self):
        node = PatternNode(name="test", node_class="test.nodeclass")

        self.assertIsNotNone(node)
        self.assertIsNone(node.id)
        self.assertEqual("test", node.name)
        self.assertEqual("test.nodeclass", node.node_class)
        self.assertEqual({'name': 'test', 'node_class': 'test.nodeclass'}, node.to_document())

    def test_init_with_id(self):
        node = PatternNode(name="test", node_class="test.nodeclass")
        node.id = '666'

        self.assertIsNotNone(node)
        self.assertIsNotNone(node.id)
        self.assertEqual('666', node.id)
        self.assertEqual("test", node.name)
        self.assertEqual("test.nodeclass", node.node_class)
        self.assertEqual({'_id': '666', 'name': 'test', 'node_class': 'test.nodeclass'}, node.to_document())

    def test_from_document(self):
        node1 = PatternNode.from_document(None, {'name': 'test', 'node_class': 'test.nodeclass'})
        self.assertIsNotNone(node1)
        self.assertIsNone(node1.id)
        self.assertEqual("test", node1.name)
        self.assertEqual("test.nodeclass", node1.node_class)

        node2 = PatternNode.from_document(None, {'_id': '666', 'name': 'test', 'node_class': 'test.nodeclass'})
        self.assertIsNotNone(node2)
        self.assertIsNotNone(node2.id)
        self.assertEqual('666', node2.id)
        self.assertEqual("test", node2.name)
        self.assertEqual("test.nodeclass", node2.node_class)


class TemplateNodeTests(unittest.TestCase):

    def test_init_no_id(self):
        node = TemplateNode(name="test", node_class="test.nodeclass")

        self.assertIsNotNone(node)
        self.assertIsNone(node.id)
        self.assertEqual("test", node.name)
        self.assertEqual("test.nodeclass", node.node_class)
        self.assertEqual({'name': 'test', 'node_class': 'test.nodeclass'}, node.to_document())

    def test_init_with_id(self):
        node = TemplateNode(name="test", node_class="test.nodeclass")
        node.id = '666'

        self.assertIsNotNone(node)
        self.assertIsNotNone(node.id)
        self.assertEqual('666', node.id)
        self.assertEqual("test", node.name)
        self.assertEqual("test.nodeclass", node.node_class)
        self.assertEqual({'_id': '666', 'name': 'test', 'node_class': 'test.nodeclass'}, node.to_document())

    def test_from_document(self):
        node1 = TemplateNode.from_document(None, {'name': 'test', 'node_class': 'test.nodeclass'})
        self.assertIsNotNone(node1)
        self.assertIsNone(node1.id)
        self.assertEqual("test", node1.name)
        self.assertEqual("test.nodeclass", node1.node_class)

        node2 = TemplateNode.from_document(None, {'_id': '666', 'name': 'test', 'node_class': 'test.nodeclass'})
        self.assertIsNotNone(node2)
        self.assertIsNotNone(node2.id)
        self.assertEqual('666', node2.id)
        self.assertEqual("test", node2.name)
        self.assertEqual("test.nodeclass", node2.node_class)
