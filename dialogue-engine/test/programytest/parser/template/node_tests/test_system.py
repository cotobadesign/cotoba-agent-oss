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
import os

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.system import TemplateSystemNode
from programy.parser.exceptions import ParserException

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateSystemNode(TemplateSystemNode):
    def __init__(self):
        TemplateSystemNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateSystemNodeTests(ParserTestsBaseClass):

    def test_node_no_timeout(self):

        self._client_context.brain.configuration.overrides._allow_system_aiml = True

        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSystemNode()
        self.assertIsNotNone(node)
        node.append(TemplateWordNode('echo "Hello World"'))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)

        if os.name == 'posix':
            self.assertEqual(response, "Hello World")
        elif os.name == 'nt':
                self.assertEqual(response, '"Hello World"')
        else:
            self.assertFalse(True)

    def test_node_with_timeout(self):

        self._client_context.brain.configuration.overrides._allow_system_aiml = True

        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSystemNode()
        node.timeout = 1000
        self.assertIsNotNone(node)
        node.append(TemplateWordNode('echo "Hello World"'))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        if os.name == 'posix':
            self.assertEqual(response, "Hello World")
        elif os.name == 'nt':
                self.assertEqual(response, '"Hello World"')
        else:
            self.assertFalse(True)

    def test_node_with_system_switched_off(self):

        self._client_context.brain.configuration.overrides._allow_system_aiml = False

        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSystemNode()
        node.timeout = 1000
        self.assertIsNotNone(node)
        node.append(TemplateWordNode('echo "Hello World"'))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "")

    def test_set_attrib(self):
        node = TemplateSystemNode()
        node.set_attrib("timeout", 1000)
        self.assertEqual(1000, node.timeout)

        with self.assertRaises(ParserException):
            node.set_attrib("unknown", 1000)

    def test_to_xml_no_timeout(self):
        root = TemplateNode()
        node = TemplateSystemNode()
        root.append(node)
        node.append(TemplateWordNode('echo "Hello World"'))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><system>echo "Hello World"</system></template>', xml_str)

    def test_to_xml_with_timeout(self):
        root = TemplateNode()
        node = TemplateSystemNode()
        node.timeout = 1000
        root.append(node)
        node.append(TemplateWordNode('echo "Hello World"'))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><system timeout="1000">echo "Hello World"</system></template>', xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateSystemNode()
        root.append(node)

        with self.assertRaises(Exception):
            root.resolve(self._client_context)
