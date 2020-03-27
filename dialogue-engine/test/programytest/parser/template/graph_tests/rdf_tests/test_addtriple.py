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
from programy.parser.template.nodes.addtriple import TemplateAddTripleNode
from programy.parser.exceptions import ParserException

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphAddTripleTests(TemplateGraphTestClient):

    def test_add_triple_type1(self):
        template = ET.fromstring("""
            <template>
               <addtriple>
                    <subj>X</subj>
                    <pred>Y</pred>
                    <obj>Z</obj>
                </addtriple>
            </template>
            """)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateAddTripleNode)
        self.assertEqual(0, len(ast.children[0].children))

        self.assertFalse(self._client_context.brain.rdf.has_object("X", "Y", "Z"))
        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertTrue(self._client_context.brain.rdf.has_object("X", "Y", "Z"))

    def test_add_triple_type2(self):
        template = ET.fromstring("""
            <template>
                <addtriple subj="X" pred="Y" obj="Z">
                </addtriple>
            </template>
            """)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateAddTripleNode)
        self.assertEqual(0, len(ast.children[0].children))

        self.assertFalse(self._client_context.brain.rdf.has_object("X", "Y", "Z"))
        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertTrue(self._client_context.brain.rdf.has_object("X", "Y", "Z"))

    def test_add_triple_type3(self):
        template = ET.fromstring("""
            <template>
                <addtriple subj="X" pred="Y" obj="Z" />
            </template>
            """)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateAddTripleNode)
        self.assertEqual(0, len(ast.children[0].children))

        self.assertFalse(self._client_context.brain.rdf.has_object("X", "Y", "Z"))
        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertTrue(self._client_context.brain.rdf.has_object("X", "Y", "Z"))

    def test_add_triple_no_parameter(self):
        template1 = ET.fromstring("""
            <template>
                <addtriple pred="Y" obj="Z" />
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template1)

        template2 = ET.fromstring("""
            <template>
                <addtriple subj="X" obj="Z" />
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template2)

        template3 = ET.fromstring("""
            <template>
                <addtriple subj="X" pred="Y" />
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template3)
