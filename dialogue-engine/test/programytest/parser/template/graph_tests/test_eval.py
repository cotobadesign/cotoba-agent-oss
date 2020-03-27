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
from programy.parser.template.nodes.get import TemplateGetNode
from programy.parser.template.nodes.eval import TemplateEvalNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphEvalTests(TemplateGraphTestClient):

    def test_eval_node_from_xml_single_word(self):
        template = ET.fromstring("""
            <template>
                <eval>Text</eval>
            </template>
            """)
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateEvalNode)

    def test_eval_node_from_xml_multi_words(self):
        template = ET.fromstring("""
            <template>
                <eval>Some Text</eval>
            </template>
            """)
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateEvalNode)

        self.assertEqual(len(node.children), 1)
        self.assertIsInstance(node.children[0], TemplateWordNode)
        self.assertEqual(node.children[0].word, "Some Text")

    def test_eval_node_from_xml_multi_words_get(self):
        template = ET.fromstring("""
            <template>
                <eval>Some <get name="SomeGet" /> Text</eval>
            </template>
            """)
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateEvalNode)

        self.assertEqual(len(node.children), 3)
        self.assertIsInstance(node.children[0], TemplateWordNode)
        self.assertEqual(node.children[0].word, "Some")
        self.assertIsInstance(node.children[1], TemplateGetNode)
        self.assertIsInstance(node.children[2], TemplateWordNode)
        self.assertEqual(node.children[2].word, "Text")
