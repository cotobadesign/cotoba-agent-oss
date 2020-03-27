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
from programy.parser.template.nodes.bot import TemplateBotNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateBotNode(TemplateBotNode):

    def __init__(self):
        TemplateBotNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is a failure")


class TemplateBotNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateBotNode()
        self.assertIsNotNone(node)
        node.name = TemplateWordNode("location")
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property("location", "Scotland")

        result = node.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("Scotland", result)

    def test_node_no_value(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateBotNode()
        self.assertIsNotNone(node)
        node.name = TemplateWordNode("location")
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property("default-property", "unknown")

        result = node.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateBotNode()
        node.name = TemplateWordNode("name")
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><bot name="name" /></template>', xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = MockTemplateBotNode()
        self.assertIsNotNone(node)
        node.name = TemplateWordNode("location")
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property("location", "Scotland")

        with self.assertRaises(Exception):
            node.resolve_to_string(self._client_context)

        with self.assertRaises(Exception):
            root.resolve(self._client_context)
