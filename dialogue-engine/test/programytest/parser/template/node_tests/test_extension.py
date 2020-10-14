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
from programy.parser.template.nodes.extension import TemplateExtensionNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass


class MockExtension(object):

    def execute(self, context, data):
        if data is None or data == "":
            return "VALID"
        else:
            return data


class MockTemplateExtensionNode(TemplateExtensionNode):
    def __init__(self):
        TemplateExtensionNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateExtensionNodeTests(ParserTestsBaseClass):

    def test_node_no_data(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateExtensionNode()
        self.assertIsNotNone(node)
        self.assertIsNone(node.path)

        node.path = "programytest.parser.template.node_tests.test_extension.MockExtension"
        self.assertEqual("programytest.parser.template.node_tests.test_extension.MockExtension", node.path)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual(root.resolve(self._client_context), "VALID")

    def test_node_with_data(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateExtensionNode()
        self.assertIsNotNone(node)
        self.assertIsNone(node.path)

        node.append(TemplateWordNode("Test"))

        node.path = "programytest.parser.template.node_tests.test_extension.MockExtension"
        self.assertEqual("programytest.parser.template.node_tests.test_extension.MockExtension", node.path)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual(root.resolve(self._client_context), "Test")

    def test_node_invalid_class(self):
        root = TemplateNode()
        node = TemplateExtensionNode()
        node.path = "programytest.parser.template.node_tests.test_extension.MockExtensionOther"
        root.append(node)

        with self.assertRaises(Exception):
            root.resolve(self._client_context)

    def test_to_xml(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateExtensionNode()
        node.path = "programytest.parser.template.node_tests.test_extension.MockExtension"
        node.append(TemplateWordNode("Test"))
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><extension path="programytest.parser.template.node_tests.test_extension.MockExtension">Test</extension></template>', xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateExtensionNode()
        root.append(node)

        with self.assertRaises(Exception):
            root.resolve(self._client_context)
