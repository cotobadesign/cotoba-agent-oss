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
from programy.parser.template.nodes.select import TemplateSelectNode, Query, NotQuery

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateSelectNode(TemplateSelectNode):
    def __init__(self):
        TemplateSelectNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateSelectNodeTests(ParserTestsBaseClass):

    def test_to_string(self):
        root = TemplateSelectNode()
        self.assertIsNotNone(root)
        self.assertEqual("[SELECT]", root.to_string())

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateSelectNode()
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><select /></template>", xml_str)

    def test_to_xml_vars(self):
        root = TemplateNode()
        node = TemplateSelectNode(vars=["?x", "?y"])
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><select><vars>?x ?y</vars></select></template>", xml_str)

    def test_to_xml_query(self):
        root = TemplateNode()
        query = Query("subject", "predicate", "object")
        node = TemplateSelectNode(queries=[query])

        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><select><q><subj>subject</subj><pred>predicate</pred><obj>object</obj></q></select></template>", xml_str)

    def test_to_xml_not_query(self):
        root = TemplateNode()
        not_query = NotQuery("subject", "predicate", "object")
        node = TemplateSelectNode(queries=[not_query])

        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><select><notq><subj>subject</subj><pred>predicate</pred><obj>object</obj></notq></select></template>", xml_str)

    def test_node_default(self):
        root = TemplateNode()
        node = TemplateSelectNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateSelectNode()
        root.append(node)

        with self.assertRaises(Exception):
            root.resolve(self._client_context)
