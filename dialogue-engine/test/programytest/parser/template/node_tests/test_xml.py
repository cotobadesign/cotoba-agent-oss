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
from programy.parser.template.nodes.xml import TemplateXMLNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateXMLNode(TemplateXMLNode):
    def __init__(self):
        TemplateXMLNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateXMLNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        xml = TemplateXMLNode()
        xml._name = "dial"
        root.append(xml)

        xml.append(TemplateWordNode("07777777777"))

        self.assertEqual(len(root.children), 1)

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual("<dial>07777777777</dial>", resolved)

    def test_node_with_attribs(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        xml = TemplateXMLNode()
        xml._name = "dial"
        xml._attribs['leave_message'] = "true"
        root.append(xml)

        xml.append(TemplateWordNode("07777777777"))

        self.assertEqual(len(root.children), 1)

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual('<dial leave_message="true">07777777777</dial>', resolved)

    def test_to_xml(self):
        root = TemplateNode()
        xml = TemplateXMLNode()
        xml._name = "dial"
        root.append(xml)
        xml.append(TemplateWordNode("07777777777"))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><dial>07777777777</dial></template>", xml_str)

    def test_to_xml_with_attribs(self):
        root = TemplateNode()
        xml = TemplateXMLNode()
        xml._name = "dial"
        xml._attribs['leave_message'] = "true"
        root.append(xml)
        xml.append(TemplateWordNode("07777777777"))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><dial leave_message="true">07777777777</dial></template>', xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateXMLNode()
        root.append(node)

        with self.assertRaises(Exception):
            root.resolve(self._client_context)
