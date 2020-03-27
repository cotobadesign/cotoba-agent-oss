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
from programy.parser.template.nodes.nluintent import TemplateNluIntentNode
from programy.parser.exceptions import ParserException

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphNluIntentTests(TemplateGraphTestClient):

    def test_nluintent_template_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <nluintent name="nlu_intent" item="score" />
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        nluintent_node = ast.children[0]
        self.assertIsNotNone(nluintent_node)
        self.assertIsInstance(nluintent_node, TemplateNluIntentNode)
        self.assertIsNotNone(nluintent_node._intentName)
        self.assertIsNotNone(nluintent_node._itemName)
        self.assertIsNone(nluintent_node._index)
        self.assertIsInstance(nluintent_node._intentName, TemplateNode)
        self.assertIsInstance(nluintent_node._itemName, TemplateNode)
        self.assertEqual(nluintent_node._intentName.resolve(self._client_context), "nlu_intent")
        self.assertEqual(nluintent_node._itemName.resolve(self._client_context), "score")

    def test_nluintent_template_as_attrib_with_index(self):
        template = ET.fromstring("""
            <template>
                <nluintent name="*" item="score" index="0" />
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        nluintent_node = ast.children[0]
        self.assertIsNotNone(nluintent_node)
        self.assertIsInstance(nluintent_node, TemplateNluIntentNode)
        self.assertIsNotNone(nluintent_node._intentName)
        self.assertIsNotNone(nluintent_node._itemName)
        self.assertIsNotNone(nluintent_node._index)
        self.assertIsInstance(nluintent_node._intentName, TemplateNode)
        self.assertIsInstance(nluintent_node._itemName, TemplateNode)
        self.assertIsInstance(nluintent_node._index, TemplateNode)
        self.assertEqual(nluintent_node._intentName.resolve(self._client_context), "*")
        self.assertEqual(nluintent_node._itemName.resolve(self._client_context), "score")
        self.assertEqual(nluintent_node._index.resolve(self._client_context), "0")

    def test_nluintent_template_as_childlen(self):
        template = ET.fromstring("""
            <template>
                <nluintent>
                    <name>nlu_intent</name>
                    <item>score</item>
                </nluintent>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        nluintent_node = ast.children[0]
        self.assertIsNotNone(nluintent_node)
        self.assertIsInstance(nluintent_node, TemplateNluIntentNode)
        self.assertIsNotNone(nluintent_node._intentName)
        self.assertIsNotNone(nluintent_node._itemName)
        self.assertIsNone(nluintent_node._index)
        self.assertIsInstance(nluintent_node._intentName, TemplateNode)
        self.assertIsInstance(nluintent_node._itemName, TemplateNode)
        self.assertEqual(nluintent_node._intentName.resolve(self._client_context), "nlu_intent")
        self.assertEqual(nluintent_node._itemName.resolve(self._client_context), "score")

    def test_nluintent_template_as_childlen_with_index(self):
        template = ET.fromstring("""
            <template>
                <nluintent>
                    <name>*</name>
                    <item>score</item>
                    <index>0</index>
                </nluintent>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        nluintent_node = ast.children[0]
        self.assertIsNotNone(nluintent_node)
        self.assertIsInstance(nluintent_node, TemplateNluIntentNode)
        self.assertIsNotNone(nluintent_node._intentName)
        self.assertIsNotNone(nluintent_node._itemName)
        self.assertIsNotNone(nluintent_node._index)
        self.assertIsInstance(nluintent_node._intentName, TemplateNode)
        self.assertIsInstance(nluintent_node._itemName, TemplateNode)
        self.assertIsInstance(nluintent_node._index, TemplateNode)
        self.assertEqual(nluintent_node._intentName.resolve(self._client_context), "*")
        self.assertEqual(nluintent_node._itemName.resolve(self._client_context), "score")
        self.assertEqual(nluintent_node._index.resolve(self._client_context), "0")

    def test_nluintent_template_as_mixed(self):
        template = ET.fromstring("""
            <template>
                Test data
                <nluintent name="nlu_intent">
                    <item>score</item>
                </nluintent>
                yes
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 3)

        nluintent_node = ast.children[1]
        self.assertIsNotNone(nluintent_node)
        self.assertIsInstance(nluintent_node, TemplateNluIntentNode)
        self.assertIsNotNone(nluintent_node._intentName)
        self.assertIsNotNone(nluintent_node._itemName)
        self.assertIsNone(nluintent_node._index)
        self.assertIsInstance(nluintent_node._intentName, TemplateNode)
        self.assertIsInstance(nluintent_node._itemName, TemplateNode)
        self.assertEqual(nluintent_node._intentName.resolve(self._client_context), "nlu_intent")
        self.assertEqual(nluintent_node._itemName.resolve(self._client_context), "score")

    def test_nluintent_template_as_mixed_with_index(self):
        template = ET.fromstring("""
            <template>
                Test data
                <nluintent item="score">
                    <name>*</name>
                    <index>0</index>
                </nluintent>
                yes
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 3)

        nluintent_node = ast.children[1]
        self.assertIsNotNone(nluintent_node)
        self.assertIsInstance(nluintent_node, TemplateNluIntentNode)
        self.assertIsNotNone(nluintent_node._intentName)
        self.assertIsNotNone(nluintent_node._itemName)
        self.assertIsNotNone(nluintent_node._index)
        self.assertIsInstance(nluintent_node._intentName, TemplateNode)
        self.assertIsInstance(nluintent_node._itemName, TemplateNode)
        self.assertIsInstance(nluintent_node._index, TemplateNode)
        self.assertEqual(nluintent_node._intentName.resolve(self._client_context), "*")
        self.assertEqual(nluintent_node._itemName.resolve(self._client_context), "score")
        self.assertEqual(nluintent_node._index.resolve(self._client_context), "0")

    def test_nluintent_template_any_item(self):
        template1 = ET.fromstring("""
            <template>
                <nluintent name="nlu_intent" item="intent" />
            </template>
            """)
        ast1 = self._graph.parse_template_expression(template1)
        nluintent_node1 = ast1.children[0]
        self.assertEqual(nluintent_node1._intentName.resolve(self._client_context), "nlu_intent")
        self.assertEqual(nluintent_node1._itemName.resolve(self._client_context), "intent")

        template2 = ET.fromstring("""
            <template>
                <nluintent name="nlu_intent" item="score" />
            </template>
            """)
        ast2 = self._graph.parse_template_expression(template2)
        nluintent_node2 = ast2.children[0]
        self.assertEqual(nluintent_node2._intentName.resolve(self._client_context), "nlu_intent")
        self.assertEqual(nluintent_node2._itemName.resolve(self._client_context), "score")

        template3 = ET.fromstring("""
            <template>
                <nluintent name="*" item="count" />
            </template>
            """)
        ast3 = self._graph.parse_template_expression(template3)
        nluintent_node3 = ast3.children[0]
        self.assertEqual(nluintent_node3._intentName.resolve(self._client_context), "*")
        self.assertEqual(nluintent_node3._itemName.resolve(self._client_context), "count")

        template4 = ET.fromstring("""
            <template>
                <nluintent name="nlu_intent" item="any" />
            </template>
            """)
        ast4 = self._graph.parse_template_expression(template4)
        nluintent_node4 = ast4.children[0]
        self.assertEqual(nluintent_node4._intentName.resolve(self._client_context), "nlu_intent")
        self.assertEqual(nluintent_node4._itemName.resolve(self._client_context), "any")

    def test_nluintent_template_no_name(self):
        template1 = ET.fromstring("""
            <template>
                <nluintent item="score" />
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template1)

        template2 = ET.fromstring("""
            <template>
                <nluintent><item>score</item></nluintent>
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template2)

    def test_nluintent_template_no_item(self):
        template1 = ET.fromstring("""
            <template>
                <nluintent name="nlu_intent" />
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template1)

        template2 = ET.fromstring("""
            <template>
                <nluintent><name>nlu_intent</name></nluintent>
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template2)

    def test_nluintent_template_other(self):
        template = ET.fromstring("""
            <template>
                <nluintent><id>somevar</id></nluintent>
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)
