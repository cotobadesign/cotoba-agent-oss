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
import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.first import TemplateFirstNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateFirstNode(TemplateFirstNode):
    def __init__(self):
        TemplateFirstNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateFirstNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateFirstNode()
        self.assertIsNotNone(node)

        root.append(node)
        word1 = TemplateWordNode("Word1")
        node.append(word1)
        word2 = TemplateWordNode("Word2")
        node.append(word2)
        word3 = TemplateWordNode("Word3")
        node.append(word3)

        self.assertEqual(root.resolve(self._client_context), "Word1")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateFirstNode()
        root.append(node)
        word1 = TemplateWordNode("Word1")
        node.append(word1)
        word2 = TemplateWordNode("Word2")
        node.append(word2)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><first>Word1 Word2</first></template>", xml_str)

    def test_node_no_words(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateFirstNode()
        self.assertIsNotNone(node)

        root.append(node)

        self.assertEqual(root.resolve(self._client_context), "unknown")

    def test_to_xml_no_words(self):
        root = TemplateNode()
        node = TemplateFirstNode()
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><first /></template>", xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateFirstNode()
        root.append(node)

        with self.assertRaises(Exception):
            root.resolve(self._client_context)
