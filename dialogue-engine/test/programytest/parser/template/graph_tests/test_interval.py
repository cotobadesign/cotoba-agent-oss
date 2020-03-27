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

from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.interval import TemplateIntervalNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphIntervalTests(TemplateGraphTestClient):

    def test_interval_no_mandatory(self):
        template1 = ET.fromstring("""
            <template>
                <interval>Text</interval>
            </template>
            """)
        template2 = ET.fromstring("""
            <template>
                <interval>
                    <from>Wed Oct  5 16:35:11 2016</from>
                    <to>Fri Oct  7 16:35:11 2016</to>
                </interval>
            </template>
            """)
        template3 = ET.fromstring("""
            <template>
                <interval>
                    <style>days</style>
                    <to>Fri Oct  7 16:35:11 2016</to>
                </interval>
            </template>
            """)
        template4 = ET.fromstring("""
            <template>
                <interval>
                    <style>days</style>
                    <from>Wed Oct  5 16:35:11 2016</from>
                </interval>
            </template>
            """)

        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template1)

        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template2)

        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template3)

        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template4)

    def test_interval_node_from_xml(self):
        template = ET.fromstring("""
            <template>
                <interval>
                    <style>days</style>
                    <from>Wed Oct  5 16:35:11 2016</from>
                    <to>Fri Oct  7 16:35:11 2016</to>
                </interval>
            </template>
            """)

        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateIntervalNode)

    def test_interval_values_as_attribs(self):
        template = ET.fromstring("""
            <template>
                <interval>
                    <format>%c</format>
                    <style>days</style>
                    <from>Wed Oct  5 16:35:11 2016</from>
                    <to>Fri Oct  7 16:35:11 2016</to>
                </interval>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateIntervalNode)
        self.assertEqual(ast.resolve(self._client_context), "2")

    def test_interval_style_with_child(self):
        template = ET.fromstring("""
            <template>
                <interval>
                    <format>%c</format>
                    <style><lowercase>DAYS</lowercase></style>
                    <from>Wed Oct  5 16:35:11 2016</from>
                    <to>Fri Oct  7 16:35:11 2016</to>
                </interval>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateIntervalNode)
        self.assertEqual(ast.resolve(self._client_context), "2")

    def test_interval_with_child(self):
        template = ET.fromstring("""
            <template>
                <interval>
                    <format>%c</format>
                    <style>days</style>
                    <from>Wed Oct  5 16:35:11 2016</from>
                    <to>Fri Oct  7 16:35:11 2016</to>
                    <lowercase>DAYS</lowercase>
                </interval>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateIntervalNode)
        self.assertEqual(ast.resolve(self._client_context), "2")
