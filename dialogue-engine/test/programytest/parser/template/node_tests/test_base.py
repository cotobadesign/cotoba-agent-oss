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
from programy.parser.template.nodes.id import TemplateIdNode
from programy.parser.template.nodes.srai import TemplateSRAINode

from programytest.parser.base import ParserTestsBaseClass


class TemplateNodeBasicTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

    def test_node_children(self):
        node = TemplateNode()
        node.append(TemplateWordNode("Word1"))
        self.assertEqual(len(node.children), 1)
        node.append(TemplateWordNode("Word2"))
        self.assertEqual(len(node.children), 2)
        self.assertEqual("Word1 Word2", node.resolve_children_to_string(self._client_context))
        self.assertEqual("Word1 Word2", node.resolve(self._client_context))
        self.assertEqual("[NODE]", node.to_string())

    def test_to_xml_simple(self):
        node = TemplateNode()
        node.append(TemplateWordNode("Word1"))
        node.append(TemplateWordNode("Word2"))
        self.assertEqual("Word1 Word2", node.to_xml(self._client_context))

    def test_to_xml_composite(self):
        node = TemplateNode()
        node.append(TemplateWordNode("Word1"))
        node.append(TemplateIdNode())
        srai = TemplateSRAINode()
        srai.append(TemplateWordNode("Srai1"))
        node.append(srai)
        node.append(TemplateWordNode("Word2"))
        self.assertEqual("Word1<id /><srai>Srai1</srai>Word2", node.to_xml(self._client_context))

    def test_xml_tree_simple(self):
        node = TemplateNode()
        node.append(TemplateWordNode("Word1"))
        node.append(TemplateWordNode("Word2"))
        xml = node.xml_tree(self._client_context)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template>Word1 Word2</template>", xml_str)

    def test_xml_tree_simple_composite(self):
        node = TemplateNode()
        node.append(TemplateWordNode("Word1"))
        node.append(TemplateIdNode())
        srai = TemplateSRAINode()
        srai.append(TemplateWordNode("Srai1"))
        node.append(srai)
        node.append(TemplateWordNode("Word2"))
        xml = node.xml_tree(self._client_context)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template>Word1<id /><srai>Srai1</srai>Word2</template>", xml_str)
