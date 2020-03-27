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
from programy.parser.template.nodes.nluslot import TemplateNluSlotNode
from programy.parser.exceptions import ParserException

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphNluSlotTests(TemplateGraphTestClient):

    def test_nluslot_template_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <nluslot name="nlu_slot" item="entity" />
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        nluslot_node = ast.children[0]
        self.assertIsNotNone(nluslot_node)
        self.assertIsInstance(nluslot_node, TemplateNluSlotNode)
        self.assertIsNotNone(nluslot_node._slotName)
        self.assertIsNotNone(nluslot_node._itemName)
        self.assertIsNone(nluslot_node._index)
        self.assertIsInstance(nluslot_node._slotName, TemplateNode)
        self.assertIsInstance(nluslot_node._itemName, TemplateNode)
        self.assertEqual(nluslot_node._slotName.resolve(self._client_context), "nlu_slot")
        self.assertEqual(nluslot_node._itemName.resolve(self._client_context), "entity")

    def test_nluslot_template_as_attrib_with_index(self):
        template = ET.fromstring("""
            <template>
                <nluslot name="*" item="entity" index="0" />
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        nluslot_node = ast.children[0]
        self.assertIsNotNone(nluslot_node)
        self.assertIsInstance(nluslot_node, TemplateNluSlotNode)
        self.assertIsNotNone(nluslot_node._slotName)
        self.assertIsNotNone(nluslot_node._itemName)
        self.assertIsNotNone(nluslot_node._index)
        self.assertIsInstance(nluslot_node._slotName, TemplateNode)
        self.assertIsInstance(nluslot_node._itemName, TemplateNode)
        self.assertIsInstance(nluslot_node._index, TemplateNode)
        self.assertEqual(nluslot_node._slotName.resolve(self._client_context), "*")
        self.assertEqual(nluslot_node._itemName.resolve(self._client_context), "entity")
        self.assertEqual(nluslot_node._index.resolve(self._client_context), "0")

    def test_nluslot_template_as_childlen(self):
        template = ET.fromstring("""
            <template>
                <nluslot>
                    <name>nlu_slot</name>
                    <item>entity</item>
                </nluslot>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        nluslot_node = ast.children[0]
        self.assertIsNotNone(nluslot_node)
        self.assertIsInstance(nluslot_node, TemplateNluSlotNode)
        self.assertIsNotNone(nluslot_node._slotName)
        self.assertIsNotNone(nluslot_node._itemName)
        self.assertIsNone(nluslot_node._index)
        self.assertIsInstance(nluslot_node._slotName, TemplateNode)
        self.assertIsInstance(nluslot_node._itemName, TemplateNode)
        self.assertEqual(nluslot_node._slotName.resolve(self._client_context), "nlu_slot")
        self.assertEqual(nluslot_node._itemName.resolve(self._client_context), "entity")

    def test_nluslot_template_as_childlen_with_index(self):
        template = ET.fromstring("""
            <template>
                <nluslot>
                    <name>*</name>
                    <item>entity</item>
                    <index>0</index>
                </nluslot>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        nluslot_node = ast.children[0]
        self.assertIsNotNone(nluslot_node)
        self.assertIsInstance(nluslot_node, TemplateNluSlotNode)
        self.assertIsNotNone(nluslot_node._slotName)
        self.assertIsNotNone(nluslot_node._itemName)
        self.assertIsNotNone(nluslot_node._index)
        self.assertIsInstance(nluslot_node._slotName, TemplateNode)
        self.assertIsInstance(nluslot_node._itemName, TemplateNode)
        self.assertIsInstance(nluslot_node._index, TemplateNode)
        self.assertEqual(nluslot_node._slotName.resolve(self._client_context), "*")
        self.assertEqual(nluslot_node._itemName.resolve(self._client_context), "entity")
        self.assertEqual(nluslot_node._index.resolve(self._client_context), "0")

    def test_nluslot_template_as_mixed(self):
        template = ET.fromstring("""
            <template>
                Test data
                <nluslot name="nlu_slot">
                    <item>entity</item>
                </nluslot>
                yes
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 3)

        nluslot_node = ast.children[1]
        self.assertIsNotNone(nluslot_node)
        self.assertIsInstance(nluslot_node, TemplateNluSlotNode)
        self.assertIsNotNone(nluslot_node._slotName)
        self.assertIsNotNone(nluslot_node._itemName)
        self.assertIsNone(nluslot_node._index)
        self.assertIsInstance(nluslot_node._slotName, TemplateNode)
        self.assertIsInstance(nluslot_node._itemName, TemplateNode)
        self.assertEqual(nluslot_node._slotName.resolve(self._client_context), "nlu_slot")
        self.assertEqual(nluslot_node._itemName.resolve(self._client_context), "entity")

    def test_nluslot_template_as_mixed_with_index(self):
        template = ET.fromstring("""
            <template>
                Test data
                <nluslot name="*">
                    <item>entity</item>
                    <index>0</index>
                </nluslot>
                yes
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 3)

        nluslot_node = ast.children[1]
        self.assertIsNotNone(nluslot_node)
        self.assertIsInstance(nluslot_node, TemplateNluSlotNode)
        self.assertIsNotNone(nluslot_node._slotName)
        self.assertIsNotNone(nluslot_node._itemName)
        self.assertIsNotNone(nluslot_node._index)
        self.assertIsInstance(nluslot_node._slotName, TemplateNode)
        self.assertIsInstance(nluslot_node._itemName, TemplateNode)
        self.assertIsInstance(nluslot_node._index, TemplateNode)
        self.assertEqual(nluslot_node._slotName.resolve(self._client_context), "*")
        self.assertEqual(nluslot_node._itemName.resolve(self._client_context), "entity")
        self.assertEqual(nluslot_node._index.resolve(self._client_context), "0")

    def test_nluslot_template_any_item(self):
        template1 = ET.fromstring("""
            <template>
                <nluslot name="nlu_slot" item="slot" />
            </template>
            """)
        ast1 = self._graph.parse_template_expression(template1)
        nluslot_node1 = ast1.children[0]
        self.assertEqual(nluslot_node1._slotName.resolve(self._client_context), "nlu_slot")
        self.assertEqual(nluslot_node1._itemName.resolve(self._client_context), "slot")

        template2 = ET.fromstring("""
            <template>
                <nluslot name="nlu_slot" item="entity" />
            </template>
            """)
        ast2 = self._graph.parse_template_expression(template2)
        nluslot_node2 = ast2.children[0]
        self.assertEqual(nluslot_node2._slotName.resolve(self._client_context), "nlu_slot")
        self.assertEqual(nluslot_node2._itemName.resolve(self._client_context), "entity")

        template3 = ET.fromstring("""
            <template>
                <nluslot name="nlu_slot" item="score" />
            </template>
            """)
        ast3 = self._graph.parse_template_expression(template3)
        nluslot_node3 = ast3.children[0]
        self.assertEqual(nluslot_node3._slotName.resolve(self._client_context), "nlu_slot")
        self.assertEqual(nluslot_node3._itemName.resolve(self._client_context), "score")

        template4 = ET.fromstring("""
            <template>
                <nluslot name="nlu_slot" item="startOffset" />
            </template>
            """)
        ast4 = self._graph.parse_template_expression(template4)
        nluslot_node4 = ast4.children[0]
        self.assertEqual(nluslot_node4._slotName.resolve(self._client_context), "nlu_slot")
        self.assertEqual(nluslot_node4._itemName.resolve(self._client_context), "startOffset")

        template5 = ET.fromstring("""
            <template>
                <nluslot name="nlu_slot" item="endOffset" />
            </template>
            """)
        ast5 = self._graph.parse_template_expression(template5)
        nluslot_node5 = ast5.children[0]
        self.assertEqual(nluslot_node5._slotName.resolve(self._client_context), "nlu_slot")
        self.assertEqual(nluslot_node5._itemName.resolve(self._client_context), "endOffset")

        template6 = ET.fromstring("""
            <template>
                <nluslot name="*" item="count" />
            </template>
            """)
        ast6 = self._graph.parse_template_expression(template6)
        nluslot_node6 = ast6.children[0]
        self.assertEqual(nluslot_node6._slotName.resolve(self._client_context), "*")
        self.assertEqual(nluslot_node6._itemName.resolve(self._client_context), "count")

        template7 = ET.fromstring("""
            <template>
                <nluslot name="nlu_slot" item="any" />
            </template>
            """)
        ast7 = self._graph.parse_template_expression(template7)
        nluslot_node7 = ast7.children[0]
        self.assertEqual(nluslot_node7._slotName.resolve(self._client_context), "nlu_slot")
        self.assertEqual(nluslot_node7._itemName.resolve(self._client_context), "any")

    def test_nluslot_template_no_name(self):
        template1 = ET.fromstring("""
            <template>
                <nluslot item="entity" />
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template1)

        template2 = ET.fromstring("""
            <template>
                <nluslot><item>entity</item></nluslot>
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template2)

    def test_nluslot_template_no_item(self):
        template1 = ET.fromstring("""
            <template>
                <nluslot name="nlu_slot" />
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template1)

        template2 = ET.fromstring("""
            <template>
                <nluslot><name>nlu_slot</name></nluslot>
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template2)

    def test_nluslot_template_other(self):
        template = ET.fromstring("""
            <template>
                <nluslot><id>somevar</id></nluslot>
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)
