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
from programy.parser.template.nodes.set import TemplateSetNode
from programy.parser.exceptions import ParserException

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphSetTests(TemplateGraphTestClient):

    def test_set_template_typename_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <set name="somepred">Value1</set>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(self._client_context), "somepred")
        self.assertEqual(set_node.property_type, "name")

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(self._client_context), "Value1")

    def test_set_template_multi_word_typename_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <set name="somepred other">Value1</set>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(self._client_context), "somepred other")
        self.assertEqual(set_node.property_type, "name")

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(self._client_context), "Value1")

    def test_set_template_typename_nested(self):
        template = ET.fromstring("""
            <template>
                Some text here
                <set name="somepred">Value1</set>
                Some text there
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 3)

        set_node = ast.children[1]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(self._client_context), "somepred")
        self.assertEqual(set_node.property_type, "name")

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(self._client_context), "Value1")

    def test_set_template_typedata_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <set data="somedata">Value2</set>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(self._client_context), "somedata")
        self.assertEqual(set_node.property_type, "data")

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(self._client_context), "Value2")

    def test_set_template_typevar_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <set var="somevar">Value3</set>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(self._client_context), "somevar")
        self.assertEqual(set_node.property_type, "var")

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(self._client_context), "Value3")

    def test_set_template_typename_as_child(self):
        template = ET.fromstring("""
            <template>
                <set><name>somepred</name>Value4</set>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(self._client_context), "somepred")
        self.assertEqual(set_node.property_type, "name")

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(self._client_context), "Value4")

    def test_set_template_typedata_as_child(self):
        template = ET.fromstring("""
            <template>
                <set><data>somedata</data>Value5</set>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(self._client_context), "somedata")
        self.assertEqual(set_node.property_type, "data")

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(self._client_context), "Value5")

    def test_set_template_typevar_as_child(self):
        template = ET.fromstring("""
            <template>
                <set><var>somevar</var>Value6</set>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(self._client_context), "somevar")
        self.assertEqual(set_node.property_type, "var")

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(self._client_context), "Value6")

    def test_set_type_name_and_var(self):
        template = ET.fromstring("""
                <template>
                    <set name="somepred" var="somevar">Value1</set>
                </template>
                """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)

    def test_set_type_name_and_data(self):
        template = ET.fromstring("""
                <template>
                    <set name="somepred" data="somedata">Value1</set>
                </template>
                """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)

    def test_set_type_data_and_var(self):
        template = ET.fromstring("""
                <template>
                    <set data="somedata" var="somevar">Value1</set>
                </template>
                """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)

    def test_set_other(self):
        template = ET.fromstring("""
                <template>
                    <set>Value1</set>
                </template>
                """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)
