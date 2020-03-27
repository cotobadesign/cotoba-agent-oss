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
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.indexed import TemplateIndexedNode
from programy.parser.template.nodes.indexed import TemplateDoubleIndexedNode
from programy.parser.exceptions import ParserException

from programytest.parser.base import ParserTestsBaseClass


class TemplateIndexedNodeTests(ParserTestsBaseClass):

    def test_init(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIndexedNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

    def test_get_set(self):
        node = TemplateIndexedNode()
        node.index = 3
        self.assertEqual(3, node.index)
        node.index = 4
        self.assertEqual(4, node.index)

    def test_attrib_name_index_only(self):
        node = TemplateIndexedNode()
        node.set_attrib('index', 3)
        self.assertEqual(3, node.index)

    def test_invalid_attrib_name(self):
        with self.assertRaises(Exception):
            node = TemplateIndexedNode()
            node.set_attrib('rubbish', 3)


class TemplateDoubleIndexedNodeTests(ParserTestsBaseClass):

    def test_init(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateDoubleIndexedNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

    def test_get_set(self):
        node = TemplateDoubleIndexedNode()
        node.index = 3
        self.assertEqual(3, node.index)
        node.index = 4
        self.assertEqual(4, node.index)

    def test_attrib_name_position_and_index(self):
        node = TemplateDoubleIndexedNode()
        node.set_attrib('index', "1,3")
        self.assertEqual(1, node.question)
        self.assertEqual(3, node.sentence)

    def test_attrib_name_position_and_index_as_star(self):
        node = TemplateDoubleIndexedNode()
        node.set_attrib('index', "1,*")
        self.assertEqual(1, node.question)
        self.assertEqual(-1, node.sentence)

    def test_attrib_name_position_and_index_invalid(self):
        node = TemplateDoubleIndexedNode()

        with self.assertRaises(ParserException):
            node.set_attrib('index', "1 3")

        with self.assertRaises(ParserException):
            node.set_attrib('index', "0,1")

        with self.assertRaises(ParserException):
            node.set_attrib('index', "1,0")

        with self.assertRaises(ParserException):
            node.set_attrib('index', "0,0")

        with self.assertRaises(ParserException):
            node.set_attrib('index', "1,x")

        with self.assertRaises(ParserException):
            node.set_attrib('index', "x,1")

        with self.assertRaises(ParserException):
            node.set_attrib('index', "x,x")
