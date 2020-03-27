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
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.uniq import TemplateUniqNode

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateUniqNode(TemplateUniqNode):
    def __init__(self):
        TemplateUniqNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateUniqNodeTests(ParserTestsBaseClass):

    def test_to_string(self):
        root = TemplateUniqNode()
        self.assertIsNotNone(root)
        self.assertEqual("[UNIQ]", root.to_string())

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateUniqNode(subj=TemplateWordNode("S"), pred=TemplateWordNode("P"), obj=TemplateWordNode("O"))
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><uniq><subj>S</subj><pred>P</pred><obj>O</obj></uniq></template>", xml_str)

    def test_node_defaults(self):
        root = TemplateNode()
        node = TemplateUniqNode()

        root.append(node)
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_node_no_defaults(self):
        root = TemplateNode()
        node = TemplateUniqNode(subj=TemplateWordNode("S"), pred=TemplateWordNode("P"), obj=TemplateWordNode("O"))

        root.append(node)
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateUniqNode()
        root.append(node)

        with self.assertRaises(Exception):
            root.resolve(self._client_context)
