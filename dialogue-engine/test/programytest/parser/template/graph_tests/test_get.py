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
from programy.parser.template.nodes.get import TemplateGetNode
from programy.parser.exceptions import ParserException

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphGetTests(TemplateGraphTestClient):

    def test_get_template_typename_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <get name="somepred" />
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        get_node = ast.children[0]
        self.assertIsNotNone(get_node)
        self.assertIsInstance(get_node, TemplateGetNode)
        self.assertIsNotNone(get_node.name)
        self.assertIsInstance(get_node.name, TemplateNode)
        self.assertEqual(get_node.name.resolve(self._client_context), "somepred")
        self.assertEqual(get_node.property_type, "name")

    def test_get_template_typename_as_attrib_mixed(self):
        template = ET.fromstring("""
            <template>
                Hello <get name="somepred" /> how are you
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 3)

        get_node = ast.children[1]
        self.assertIsNotNone(get_node)
        self.assertIsInstance(get_node, TemplateGetNode)
        self.assertIsNotNone(get_node.name)
        self.assertIsInstance(get_node.name, TemplateNode)
        self.assertEqual(get_node.name.resolve(self._client_context), "somepred")
        self.assertEqual(get_node.property_type, "name")

    def test_get_template_typedata_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <get data="somedata" />
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        get_node = ast.children[0]
        self.assertIsNotNone(get_node)
        self.assertIsInstance(get_node, TemplateGetNode)
        self.assertIsNotNone(get_node.name)
        self.assertIsInstance(get_node.name, TemplateNode)
        self.assertEqual(get_node.name.resolve(self._client_context), "somedata")
        self.assertEqual(get_node.property_type, "data")

    def test_get_template_typevar_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <get var="somevar" />
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        get_node = ast.children[0]
        self.assertIsNotNone(get_node)
        self.assertIsInstance(get_node, TemplateGetNode)
        self.assertIsNotNone(get_node.name)
        self.assertIsInstance(get_node.name, TemplateNode)
        self.assertEqual(get_node.name.resolve(self._client_context), "somevar")
        self.assertEqual(get_node.property_type, "var")

    def test_get_template_typename_as_child(self):
        template = ET.fromstring("""
            <template>
                <get><name>somepred as text</name></get>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        get_node = ast.children[0]
        self.assertIsNotNone(get_node)
        self.assertIsInstance(get_node, TemplateGetNode)
        self.assertIsNotNone(get_node.name)
        self.assertIsInstance(get_node.name, TemplateNode)
        self.assertEqual(get_node.name.resolve(self._client_context), "somepred as text")
        self.assertEqual(get_node.property_type, "name")

    def test_get_template_typedata_as_child(self):
        template = ET.fromstring("""
            <template>
                <get><data>data as text</data></get>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        get_node = ast.children[0]
        self.assertIsNotNone(get_node)
        self.assertIsInstance(get_node, TemplateGetNode)
        self.assertIsNotNone(get_node.name)
        self.assertIsInstance(get_node.name, TemplateNode)
        self.assertEqual(get_node.name.resolve(self._client_context), "data as text")
        self.assertEqual(get_node.property_type, "data")

    def test_get_template_typevar_as_child(self):
        template = ET.fromstring("""
            <template>
                <get><var>somevar</var></get>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        get_node = ast.children[0]
        self.assertIsNotNone(get_node)
        self.assertIsInstance(get_node, TemplateGetNode)
        self.assertIsNotNone(get_node.name)
        self.assertIsInstance(get_node.name, TemplateNode)
        self.assertEqual(get_node.name.resolve(self._client_context), "somevar")
        self.assertEqual(get_node.property_type, "var")

    def test_get_template_type_name_and_var(self):
        template = ET.fromstring("""
            <template>
                <get name="somename" var="somevar" />
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)

    def test_get_template_type_name_and_data(self):
        template = ET.fromstring("""
            <template>
                <get name="somename" data="somedata" />
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)

    def test_get_template_type_data_and_var(self):
        template = ET.fromstring("""
            <template>
                <get data="somedata" var="somevar" />
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)

    def test_get_template_other(self):
        template = ET.fromstring("""
            <template>
                <get><id>somevar</id></get>
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)
