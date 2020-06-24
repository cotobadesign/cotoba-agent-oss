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
from programy.parser.template.nodes.map import TemplateMapNode
from programy.parser.exceptions import ParserException

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphMapTests(TemplateGraphTestClient):

    def set_collection_maps(self):
        map_dict = {"key": "value"}
        self._client_context.brain.maps.add_map("somemap", map_dict, "test_map")

    def test_map_name_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <map name="somemap">sometext</map>
            </template>
            """)
        self.set_collection_maps()
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateMapNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(self._client_context), "somemap")

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(self._client_context), "sometext")

    def test_map_name_as_child(self):
        template = ET.fromstring("""
            <template>
                <map><name>somemap</name>sometext</map>
            </template>
            """)
        self.set_collection_maps()
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateMapNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(self._client_context), "somemap")

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(self._client_context), "sometext")

    def test_map_no_name(self):
        template = ET.fromstring("""
            <template>
                <map>sometext</map>
            </template>
            """)
        self.set_collection_maps()
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)
