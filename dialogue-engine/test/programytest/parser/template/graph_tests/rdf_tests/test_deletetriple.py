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
from programy.parser.template.nodes.deletetriple import TemplateDeleteTripleNode
from programy.parser.exceptions import ParserException

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphDeleteTripleTests(TemplateGraphTestClient):

    def test_delete_triple_type1(self):
        self.assertFalse(self._client_context.brain.rdf.has_object("X", "Y", "Z"))
        self._client_context.brain.rdf.add_entity("X", "Y", "Z", "LETTERS")
        self.assertTrue(self._client_context.brain.rdf.has_object("X", "Y", "Z"))

        template = ET.fromstring("""
            <template>
                <deletetriple>
                    <subj>X</subj>
                    <pred>Y</pred>
                    <obj>Z</obj>
                </deletetriple>
            </template>
            """)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateDeleteTripleNode)
        self.assertEqual(0, len(ast.children[0].children))

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertFalse(self._client_context.brain.rdf.has_object("X", "Y", "Z"))

    def test_delete_triple_type2(self):
        self.assertFalse(self._client_context.brain.rdf.has_object("X", "Y", "Z"))
        self._client_context.brain.rdf.add_entity("X", "Y", "Z", "LETTERS")
        self.assertTrue(self._client_context.brain.rdf.has_object("X", "Y", "Z"))

        template = ET.fromstring("""
            <template>
                <deletetriple subj="X" pred="Y" obj="Z">
                </deletetriple>
            </template>
            """)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateDeleteTripleNode)
        self.assertEqual(0, len(ast.children[0].children))

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertFalse(self._client_context.brain.rdf.has_object("X", "Y", "Z"))

    def test_delete_triple_type3(self):
        self.assertFalse(self._client_context.brain.rdf.has_object("X", "Y", "Z"))
        self._client_context.brain.rdf.add_entity("X", "Y", "Z", "LETTERS")
        self.assertTrue(self._client_context.brain.rdf.has_object("X", "Y", "Z"))

        template = ET.fromstring("""
            <template>
                <deletetriple subj="X" pred="Y" obj="Z" />
            </template>
            """)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateDeleteTripleNode)
        self.assertEqual(0, len(ast.children[0].children))

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertFalse(self._client_context.brain.rdf.has_object("X", "Y", "Z"))

    def test_delete_triple_no_parameter(self):
        template1 = ET.fromstring("""
            <template>
                <deletetriple pred="Y" obj="Z" />
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template1)

        template2 = ET.fromstring("""
            <template>
                <deletetriple subj="X" />
            </template>
            """)
        ast2 = self._graph.parse_template_expression(template2)
        self.assertIsNotNone(ast2)
        self.assertIsInstance(ast2.children[0], TemplateDeleteTripleNode)
        node = ast2.children[0]
        self.assertEqual(0, len(node.children))
        self.assertIsNotNone(node._subj)
        self.assertIsNone(node._pred)
        self.assertIsNone(node._obj)

        template3 = ET.fromstring("""
            <template>
                <deletetriple subj="X" pred="Y" />
            </template>
            """)
        ast3 = self._graph.parse_template_expression(template3)
        self.assertIsNotNone(ast3)
        self.assertIsInstance(ast3.children[0], TemplateDeleteTripleNode)
        node = ast3.children[0]
        self.assertEqual(0, len(node.children))
        self.assertIsNotNone(node._subj)
        self.assertIsNotNone(node._pred)
        self.assertIsNone(node._obj)

        template4 = ET.fromstring("""
            <template>
                <deletetriple subj="X" obj="Z" />
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template4)
