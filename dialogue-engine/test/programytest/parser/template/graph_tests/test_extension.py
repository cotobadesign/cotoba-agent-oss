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
from programy.parser.template.nodes.extension import TemplateExtensionNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TestExtension(object):

    def execute(self, context, data):
        return "executed"


class TemplateGraphBotTests(TemplateGraphTestClient):

    def test_extension_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <extension path="programytest.parser.template.graph_tests.test_extension.TestExtension">
                1 2 3
                </extension>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        ext_node = ast.children[0]
        self.assertIsNotNone(ext_node)
        self.assertIsInstance(ext_node, TemplateExtensionNode)
        self.assertIsNotNone(ext_node._path)

        self.assertEqual(len(ext_node.children), 1)
        self.assertEqual("executed", ext_node.resolve(self._client_context))

    def test_extension_as_child(self):
        template = ET.fromstring("""
            <template>
                <extension>
                    <path>programytest.parser.template.graph_tests.test_extension.TestExtension</path>
                    1 2 3
                </extension>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        ext_node = ast.children[0]
        self.assertIsNotNone(ext_node)
        self.assertIsInstance(ext_node, TemplateExtensionNode)
        self.assertIsNotNone(ext_node._path)

        self.assertEqual(len(ext_node.children), 1)
        self.assertEqual("executed", ext_node.resolve(self._client_context))
