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
from programy.parser.template.nodes.json import TemplateJsonNode
from programy.parser.exceptions import ParserException

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphJsonTests(TemplateGraphTestClient):

    def test_json_template_typename(self):
        template = ET.fromstring("""
            <template>
                <json name="name_json"/>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        json_node = ast.children[0]
        self.assertIsNotNone(json_node)
        self.assertIsInstance(json_node, TemplateJsonNode)
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNone(json_node._function)
        self.assertIsNone(json_node._index)
        self.assertIsNone(json_node._item)
        self.assertIsNone(json_node._key)
        self.assertIsInstance(json_node._name, TemplateNode)
        self.assertEqual(json_node._type, 'name')
        self.assertEqual(json_node._name.resolve(self._client_context), "name_json")

    def test_json_template_typedata(self):
        template = ET.fromstring("""
            <template>
                <json data="data_json"/>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        json_node = ast.children[0]
        self.assertIsNotNone(json_node)
        self.assertIsInstance(json_node, TemplateJsonNode)
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNone(json_node._function)
        self.assertIsNone(json_node._index)
        self.assertIsNone(json_node._item)
        self.assertIsNone(json_node._key)
        self.assertIsInstance(json_node._name, TemplateNode)
        self.assertEqual(json_node._type, 'data')
        self.assertEqual(json_node._name.resolve(self._client_context), "data_json")

    def test_json_template_typevar(self):
        template = ET.fromstring("""
            <template>
                <json var="var_json"/>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        json_node = ast.children[0]
        self.assertIsNotNone(json_node)
        self.assertIsInstance(json_node, TemplateJsonNode)
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNone(json_node._function)
        self.assertIsNone(json_node._index)
        self.assertIsNone(json_node._item)
        self.assertIsNone(json_node._key)
        self.assertIsInstance(json_node._name, TemplateNode)
        self.assertEqual(json_node._type, 'var')
        self.assertEqual(json_node._name.resolve(self._client_context), "var_json")

    def test_json_template_get_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <json name="json_data" key="key_1"/>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        json_node = ast.children[0]
        self.assertIsNotNone(json_node)
        self.assertIsInstance(json_node, TemplateJsonNode)
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNone(json_node._function)
        self.assertIsNone(json_node._index)
        self.assertIsNone(json_node._item)
        self.assertIsNotNone(json_node._key)
        self.assertIsInstance(json_node._name, TemplateNode)
        self.assertEqual(json_node._type, 'name')
        self.assertIsInstance(json_node._key, TemplateNode)
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data")
        self.assertEqual(json_node._key.resolve(self._client_context), "key_1")

    def test_json_template_get_as_child(self):
        template = ET.fromstring("""
            <template>
                Test data
                <json data="json_data">
                    <key>key_1</key>
                </json>
                yes
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 3)

        json_node = ast.children[1]
        self.assertIsNotNone(json_node)
        self.assertIsInstance(json_node, TemplateJsonNode)
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNone(json_node._function)
        self.assertIsNone(json_node._index)
        self.assertIsNone(json_node._item)
        self.assertIsNotNone(json_node._key)
        self.assertIsInstance(json_node._name, TemplateNode)
        self.assertEqual(json_node._type, 'data')
        self.assertIsInstance(json_node._key, TemplateNode)
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data")
        self.assertEqual(json_node._key.resolve(self._client_context), "key_1")

    def test_json_template_get_key_in_name(self):
        template = ET.fromstring("""
            <template>
                <json data="json_data.key_1" />
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        json_node = ast.children[0]
        self.assertIsNotNone(json_node)
        self.assertIsInstance(json_node, TemplateJsonNode)
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNone(json_node._function)
        self.assertIsNone(json_node._index)
        self.assertIsNone(json_node._item)
        self.assertIsNone(json_node._key)
        self.assertIsInstance(json_node._name, TemplateNode)
        self.assertEqual(json_node._type, 'data')
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data.key_1")

    def test_json_template_get_for_item(self):
        template1 = ET.fromstring("""
            <template>
                <json name="json_data" key="key_1" item="key"/>
            </template>
            """)
        ast = self._graph.parse_template_expression(template1)
        json_node = ast.children[0]
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNone(json_node._function)
        self.assertIsNone(json_node._index)
        self.assertIsNotNone(json_node._item)
        self.assertIsNotNone(json_node._key)
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data")
        self.assertEqual(json_node._key.resolve(self._client_context), "key_1")
        self.assertEqual(json_node._item.resolve(self._client_context), "key")

        template2 = ET.fromstring("""
            <template>
                <json data="json_data">
                    <key>key_1</key>
                    <item>key</item>
                </json>
            </template>
            """)
        ast = self._graph.parse_template_expression(template2)
        json_node = ast.children[0]
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNone(json_node._function)
        self.assertIsNone(json_node._index)
        self.assertIsNotNone(json_node._item)
        self.assertIsNotNone(json_node._key)
        self.assertIsInstance(json_node._name, TemplateNode)
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data")
        self.assertEqual(json_node._key.resolve(self._client_context), "key_1")
        self.assertEqual(json_node._item.resolve(self._client_context), "key")

    def test_json_template_set(self):
        template1 = ET.fromstring("""
            <template>
                <json name="json_data.key_1">data</json>
            </template>
            """)
        ast = self._graph.parse_template_expression(template1)
        json_node = ast.children[0]
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNone(json_node._function)
        self.assertIsNone(json_node._index)
        self.assertIsNone(json_node._item)
        self.assertIsNone(json_node._key)
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data.key_1")
        self.assertEqual(json_node.resolve_children(self._client_context), "data")

        template2 = ET.fromstring("""
            <template>
                <json data="json_data.key_1">
                    data
                </json>
            </template>
            """)
        ast = self._graph.parse_template_expression(template2)
        json_node = ast.children[0]
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNone(json_node._function)
        self.assertIsNone(json_node._index)
        self.assertIsNone(json_node._item)
        self.assertIsNone(json_node._key)
        self.assertIsInstance(json_node._name, TemplateNode)
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data.key_1")
        self.assertEqual(json_node.resolve_children(self._client_context), "data")

    def test_json_template_insert(self):
        template1 = ET.fromstring("""
            <template>
                <json name="json_data.key_1" function="insert" index="0">data</json>
            </template>
            """)
        ast = self._graph.parse_template_expression(template1)
        json_node = ast.children[0]
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNotNone(json_node._function)
        self.assertIsNotNone(json_node._index)
        self.assertIsNone(json_node._item)
        self.assertIsNone(json_node._key)
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data.key_1")
        self.assertEqual(json_node._function.resolve(self._client_context), "insert")
        self.assertEqual(json_node._index.resolve(self._client_context), "0")
        self.assertEqual(json_node.resolve_children(self._client_context), "data")

        template2 = ET.fromstring("""
            <template>
                <json data="json_data.key_1">
                    <function>insert</function>
                    <index>0</index>
                    data
                </json>
            </template>
            """)
        ast = self._graph.parse_template_expression(template2)
        json_node = ast.children[0]
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNotNone(json_node._function)
        self.assertIsNotNone(json_node._index)
        self.assertIsNone(json_node._item)
        self.assertIsNone(json_node._key)
        self.assertIsInstance(json_node._name, TemplateNode)
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data.key_1")
        self.assertEqual(json_node._function.resolve(self._client_context), "insert")
        self.assertEqual(json_node._index.resolve(self._client_context), "0")
        self.assertEqual(json_node.resolve_children(self._client_context), "data")

    def test_json_template_delete(self):
        template1 = ET.fromstring("""
            <template>
                <json name="json_data.key_1" function="delete" />
            </template>
            """)
        ast = self._graph.parse_template_expression(template1)
        json_node = ast.children[0]
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNotNone(json_node._function)
        self.assertIsNone(json_node._index)
        self.assertIsNone(json_node._item)
        self.assertIsNone(json_node._key)
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data.key_1")
        self.assertEqual(json_node._function.resolve(self._client_context), "delete")

        template2 = ET.fromstring("""
            <template>
                <json data="json_data.key_1">
                    <function>delete</function>
                </json>
            </template>
            """)
        ast = self._graph.parse_template_expression(template2)
        json_node = ast.children[0]
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNotNone(json_node._function)
        self.assertIsNone(json_node._index)
        self.assertIsNone(json_node._item)
        self.assertIsNone(json_node._key)
        self.assertIsInstance(json_node._name, TemplateNode)
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data.key_1")
        self.assertEqual(json_node._function.resolve(self._client_context), "delete")

    def test_json_template_set_list(self):
        template = ET.fromstring("""
            <template>
                <json name="json_data.key_1">"data1", "data2"</json>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        json_node = ast.children[0]
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNone(json_node._function)
        self.assertIsNone(json_node._index)
        self.assertIsNone(json_node._item)
        self.assertIsNone(json_node._key)
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data.key_1")
        self.assertEqual(json_node.resolve_children(self._client_context), '"data1", "data2"')

    def test_json_template_set_escape_list(self):
        template = ET.fromstring("""
            <template>
                <json name="json_data.key_1">"data1", "dat\\"a2"</json>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        json_node = ast.children[0]
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNone(json_node._function)
        self.assertIsNone(json_node._index)
        self.assertIsNone(json_node._item)
        self.assertIsNone(json_node._key)
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data.key_1")
        self.assertEqual(json_node.resolve_children(self._client_context), '"data1", "dat\\"a2"')

    def test_json_template_list_empty_data(self):
        template = ET.fromstring("""
            <template>
                <json name="json_data.key_1" function="insert" index="1">"", "", "data3"</json>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        json_node = ast.children[0]
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNotNone(json_node._function)
        self.assertIsNotNone(json_node._index)
        self.assertIsNone(json_node._item)
        self.assertIsNone(json_node._key)
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data.key_1")
        self.assertEqual(json_node.resolve_children(self._client_context), '"", "", "data3"')

    def test_json_template_set_jsonform(self):
        template = ET.fromstring("""
            <template>
                <json name="json_data.key_1">{"key1": "data1", "key2": "data2"}</json>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        json_node = ast.children[0]
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNone(json_node._function)
        self.assertIsNone(json_node._index)
        self.assertIsNone(json_node._item)
        self.assertIsNone(json_node._key)
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data.key_1")
        self.assertEqual(json_node.resolve_children(self._client_context), '{"key1": "data1", "key2": "data2"}')

    def test_json_template_invalid_type(self):
        template = ET.fromstring("""
            <template>
                <json val="somejson" />
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)

    def test_json_template_invalid_function(self):
        template = ET.fromstring("""
            <template>
                <json name="json_data.key_1" function="copy" />
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)

    def test_json_template_invalid_index(self):
        template = ET.fromstring("""
            <template>
                <json name="json_data.key_1" function="insert" index="x">data</json>
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)

    def test_json_template_invalid_list_format(self):
        template = ET.fromstring("""
            <template>
                <json name="json_data.key_1" function="insert" index="1">data1, data2</json>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        json_node = ast.children[0]
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data.key_1")
        self.assertEqual(json_node.resolve_children(self._client_context), "data1, data2")

    def test_json_template_invalid_list_quote(self):
        template = ET.fromstring("""
            <template>
                <json name="json_data.key_1" function="insert" index="1">'data1', 'data2'</json>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        json_node = ast.children[0]
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data.key_1")
        self.assertEqual(json_node.resolve_children(self._client_context), "'data1', 'data2'")

    def test_json_template_type_name_and_data(self):
        template = ET.fromstring("""
            <template>
                <json name="json_name.data.key_1" data="json_data" />
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)

    def test_json_template_type_name_and_var(self):
        template = ET.fromstring("""
            <template>
                <json var="json_var" name="json_name" />
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)

    def test_json_template_type_data_and_var(self):
        template = ET.fromstring("""
            <template>
                <json data="json_data" var="json_var" />
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)

    def test_json_template_child_node(self):
        template = ET.fromstring("""
            <template>
                <json name="json_data.key_1"><get name="get_data" /></json>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        json_node = ast.children[0]
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNone(json_node._function)
        self.assertIsNone(json_node._index)
        self.assertIsNone(json_node._item)
        self.assertIsNone(json_node._key)
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data.key_1")

    def test_json_template_child_node_after_text(self):
        template = ET.fromstring("""
            <template>
                <json name="json_data.key_1">result=<get name="get_data" /></json>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        json_node = ast.children[0]
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNone(json_node._function)
        self.assertIsNone(json_node._index)
        self.assertIsNone(json_node._item)
        self.assertIsNone(json_node._key)
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data.key_1")

    def test_json_template_child_node_before_text(self):
        template = ET.fromstring("""
            <template>
                <json name="json_data.key_1"><get name="get_data" />is OK</json>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        json_node = ast.children[0]
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNone(json_node._function)
        self.assertIsNone(json_node._index)
        self.assertIsNone(json_node._item)
        self.assertIsNone(json_node._key)
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data.key_1")

    def test_json_template_child_node_both_text(self):
        template = ET.fromstring("""
            <template>
                <json name="json_data.key_1">result=<get name="get_data" />is OK</json>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        json_node = ast.children[0]
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNone(json_node._function)
        self.assertIsNone(json_node._index)
        self.assertIsNone(json_node._item)
        self.assertIsNone(json_node._key)
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data.key_1")

    def test_json_template_list_child_node(self):
        template = ET.fromstring("""
            <template>
                <json name="json_data.key_1">"value1", "<get name="get_data" />"</json>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        json_node = ast.children[0]
        self.assertIsNotNone(json_node._name)
        self.assertIsNotNone(json_node._type)
        self.assertIsNone(json_node._function)
        self.assertIsNone(json_node._index)
        self.assertIsNone(json_node._item)
        self.assertIsNone(json_node._key)
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data.key_1")

    def test_json_template_list_child_node_error(self):
        template = ET.fromstring("""
            <template>
                <json name="json_data.key_1">"value1", <get name="get_data" /></json>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        json_node = ast.children[0]
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data.key_1")
        json_data = '\"value1\", ' + TemplateJsonNode.JSON_CHILD_IN + 'unknown' + TemplateJsonNode.JSON_CHILD_OUT
        self.assertEqual(json_node.resolve_children(self._client_context), json_data)

    def test_json_template_invalid_child_node(self):
        template = ET.fromstring("""
            <template>
                <json name="json_data.key_1">{"key": "<get name="get_data" />"}</json>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        json_node = ast.children[0]
        self.assertEqual(json_node._name.resolve(self._client_context), "json_data.key_1")
        json_data = '{\"key\": "' + TemplateJsonNode.JSON_CHILD_IN + 'unknown' + TemplateJsonNode.JSON_CHILD_OUT + '"}'
        self.assertEqual(json_node.resolve_children(self._client_context), json_data)

    def test_json_template_other(self):
        template = ET.fromstring("""
            <template>
                <json><id>somevar</id></json>
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)
