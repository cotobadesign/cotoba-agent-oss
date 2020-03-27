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
from programy.parser.template.nodes.condition import TemplateConditionNode
from programy.parser.template.nodes.condition import TemplateConditionListItemNode
from programy.parser.template.nodes.condition import TemplateConditionVariable
from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphConditionTests(TemplateGraphTestClient):

    ##################################################################################################################
    # Block (type1)
    #

    def test_condition_template_block_typename_attributes(self):
        template = ET.fromstring("""
            <template>
                <condition name="aname" value="avalue">
                    X
                    <random>
                        <li>1</li>
                        <li>2</li>
                    </random>
                    Y
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(template_node.loop)
        self.assertEqual(len(template_node.children), 3)

    def test_condition_template_block_typedata_attributes(self):
        template = ET.fromstring("""
            <template>
                <condition data="aname" value="avalue">
                    X
                    <random>
                        <li>1</li>
                        <li>2</li>
                    </random>
                    Y
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.DATA)
        self.assertFalse(template_node.loop)
        self.assertEqual(len(template_node.children), 3)

    def test_condition_template_block_typevar_attributes(self):
        template = ET.fromstring("""
            <template>
                <condition var="aname" value="avalue">
                    X
                    <random>
                        <li>1</li>
                        <li>2</li>
                    </random>
                    Y
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.LOCAL)
        self.assertEqual(len(template_node.children), 3)

    def test_condition_template_block_bot_attributes(self):
        template = ET.fromstring("""
            <template>
                <condition bot="aname" value="avalue">
                    X
                    <random>
                        <li>1</li>
                        <li>2</li>
                    </random>
                    Y
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.BOT)
        self.assertEqual(len(template_node.children), 3)

    def test_condition_template_block_typename_name_attr_val_child(self):
        template = ET.fromstring("""
            <template>
                <condition name="aname">
                    <value>avalue</value>
                    X
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_block_typedata_name_attr_val_child(self):
        template = ET.fromstring("""
            <template>
                <condition data="aname">
                    <value>avalue</value>
                    X
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.DATA)
        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_block_typevar_name_attr_val_child(self):
        template = ET.fromstring("""
            <template>
                <condition var="aname">
                    <value>avalue</value>
                    X
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.LOCAL)
        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_block_bot_name_attr_val_child(self):
        template = ET.fromstring("""
            <template>
                <condition bot="aname">
                    <value>avalue</value>
                    X
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.BOT)
        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_block_typename_name_child_val_attr(self):
        template = ET.fromstring("""
            <template>
                <condition value="avalue">
                    <name>aname</name>
                    X
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_block_typedata_name_child_val_attr(self):
        template = ET.fromstring("""
            <template>
                <condition value="avalue">
                    <data>aname</data>
                    X
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.DATA)
        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_block_typevar_name_child_val_attr(self):
        template = ET.fromstring("""
            <template>
                <condition value="avalue"><var>aname</var>X</condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.LOCAL)
        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_block_bot_name_child_val_attr(self):
        template = ET.fromstring("""
            <template>
                <condition value="avalue">
                    <bot>aname</bot>
                    X
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.BOT)
        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_block_typename_name_child_val_child(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <name>aname</name>
                    <value>avalue</value>
                    X
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_block_typedata_name_child_val_child(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <data>aname</data>
                    <value>avalue</value>
                    X
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.DATA)
        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_block_typevar_name_child_val_child(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <var>aname</var>
                    <value>avalue</value>
                    X
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.LOCAL)
        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_block_bot_name_child_val_child(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <bot>aname</bot>
                    <value>avalue</value>
                    X
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)

        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertIsInstance(template_node.value, TemplateNode)
        self.assertFalse(template_node.loop)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.BOT)
        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_duplicate_typename(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <name>aname</name>
                    <value>avalue</value>
                    <name>aname</name>
                </condition>
            </template>
            """)
        with self.assertRaises(Exception):
            self._graph.parse_template_expression(template)

    def test_condition_template_duplicate_typedata(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <data>aname</data>
                    <value>avalue</value>
                    <data>aname</data>
                </condition>
            </template>
            """)
        with self.assertRaises(Exception):
            self._graph.parse_template_expression(template)

    def test_condition_template_duplicate_typevar(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <var>aname</var>
                    <value>avalue</value>
                    <var>aname</var>
                </condition>
            </template>
            """)
        with self.assertRaises(Exception):
            self._graph.parse_template_expression(template)

    def test_condition_template_duplicate_typebot(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <bot>aname</bot>
                    <value>avalue</value>
                    <bot>aname</bot>
                </condition>
            </template>
            """)
        with self.assertRaises(Exception):
            self._graph.parse_template_expression(template)

    def test_condition_template_block_name_and_data(self):
        template = ET.fromstring("""
            <template>
                <condition name="name">
                    <data>aname</data>
                    <value>avalue</value>
                </condition>
            </template>
            """)
        with self.assertRaises(Exception):
            self._graph.parse_template_expression(template)

    def test_condition_template_block_name_and_var(self):
        template = ET.fromstring("""
            <template>
                <condition name="name">
                    <var>aname</var>
                    <value>avalue</value>
                </condition>
            </template>
            """)
        with self.assertRaises(Exception):
            self._graph.parse_template_expression(template)

    def test_condition_template_block_data_and_bot(self):
        template = ET.fromstring("""
            <template>
                <condition data="name">
                    <bot>aname</bot>
                    <value>avalue</value>
                </condition>
            </template>
            """)
        with self.assertRaises(Exception):
            self._graph.parse_template_expression(template)

    def test_condition_template_block_multi_value(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <value>avalue</value>
                    <bot>aname</bot>
                    <value>avalue</value>
                </condition>
            </template>
            """)
        with self.assertRaises(Exception):
            self._graph.parse_template_expression(template)

    def test_condition_template_block_loop(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <name>name</name>
                    <value>value</value>
                    <loop />
                </condition>
            </template>
            """)
        with self.assertRaises(Exception): 
            self._graph.parse_template_expression(template)

    def test_condition_template_block_li(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <data>name</data>
                    <value>value</value>
                    <li>X</li>
                </condition>
            </template>
            """)
        with self.assertRaises(Exception): 
            self._graph.parse_template_expression(template)

    ##################################################################################################################
    # Single (type2)
    #

    def test_condition_template_single_typename_name_child_value_attrs(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <name>aname</name>
                    <li value="a">A</li>
                    <li value="b">B</li>
                    <li><value>c</value>C</li>
                    <li>D</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertEqual(len(template_node.children), 4)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "A")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "B")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "C")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "D")

    def test_condition_template_single_typename_name_child_value_attrs_loop(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <name>aname</name>
                    <li value="a">A <loop /></li>
                    <li value="b">B</li>
                    <li><value>c</value>C</li>
                    <li>D</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertEqual(len(template_node.children), 4)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertTrue(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "A")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "B")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "C")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "D")

    def test_condition_template_single_typedata_name_child_value_attrs(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <data>aname</data>
                    <li value="a">A</li>
                    <li value="b">B</li>
                    <li><value>c</value>C</li>
                    <li>D</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.DATA)
        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertEqual(len(template_node.children), 4)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DATA)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "A")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DATA)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "B")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DATA)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "C")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DATA)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "D")

    def test_condition_template_single_typedata_name_child_value_attrs_loop(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <data>aname</data>
                    <li value="a">A</li>
                    <li value="b">B <loop /></li>
                    <li><value>c</value>C</li>
                    <li>D</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.DATA)
        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertEqual(len(template_node.children), 4)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DATA)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "A")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DATA)
        self.assertTrue(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "B")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DATA)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "C")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DATA)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "D")

    def test_condition_template_single_typevar_name_child_value_attrs(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <var>aname</var>
                    <li value="a">A</li>
                    <li value="b">B</li>
                    <li><value>c</value>C</li>
                    <li>D</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.LOCAL)
        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertEqual(len(template_node.children), 4)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "A")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "B")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "C")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "D")

    def test_condition_template_single_typevar_name_child_value_attrs_loop(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <var>aname</var>
                    <li value="a">A</li>
                    <li value="b">B</li>
                    <li><value>c</value>C <loop /></li>
                    <li>D</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.LOCAL)
        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertEqual(len(template_node.children), 4)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "A")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "B")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertTrue(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "C")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "D")

    def test_condition_template_single_typename_name_attr_value_attrs(self):
        template = ET.fromstring("""
            <template>
                <condition name="aname">
                    <li value="a">A</li>
                    <li value="b">B</li>
                    <li><value>c</value>C</li>
                    <li>D</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertEqual(len(template_node.children), 4)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "A")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "B")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "C")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "D")

    def test_condition_template_single_typedata_name_attr_value_attrs(self):
        template = ET.fromstring("""
            <template>
                <condition data="aname">
                    <li value="a">A</li>
                    <li value="b">B</li>
                    <li><value>c</value>C</li>
                    <li>D</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.DATA)
        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertEqual(len(template_node.children), 4)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DATA)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "A")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DATA)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "B")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DATA)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "C")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DATA)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "D")

    def test_condition_template_single_typevar_name_attr_value_attrs(self):
        template = ET.fromstring("""
            <template>
                <condition var="aname">
                    <li value="a">A</li>
                    <li value="b">B</li>
                    <li><value>c</value>C</li>
                    <li>D</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.LOCAL)
        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertEqual(len(template_node.children), 4)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "A")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "B")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "C")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "D")

    def test_condition_template_single_bot_name_attr_value_attrs(self):
        template = ET.fromstring("""
            <template>
                <condition bot="aname">
                    <li value="a">A</li>
                    <li value="b">B</li>
                    <li><value>c</value>C</li>
                    <li>D</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(template_node.var_type, TemplateConditionVariable.BOT)
        self.assertEqual(template_node.name.children[0].word, "aname")
        self.assertEqual(len(template_node.children), 4)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "A")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "B")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "C")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "D")

    def test_condition_template_Single_invalid_tag(self):
        template = ET.fromstring("""
            <template>
                <condition bot="aname">
                    <li value="a">A</li>
                    <li value="b">B</li>
                    <li><value>c</value>C</li>
                    <lx>D</lx>
                </condition>
            </template>
            """)
        with self.assertRaises(Exception):
            self._graph.parse_template_expression(template)

    def test_condition_template_Single_invalid_type(self):
        template = ET.fromstring("""
            <template>
                <condition bot="aname">
                    <li value="a">A</li>
                    <li value="b">B</li>
                    <li name="name1"><value>c</value>C</li>
                    <li>D</li>
                </condition>
            </template>
            """)
        with self.assertRaises(Exception):
            self._graph.parse_template_expression(template)

    ##################################################################################################################
    # Multiple (type3)
    #

    def test_condition_template_multi_typename_name_value_mixed(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <li name='name1' value="a">Val1</li>
                    <li value="b"><name>name2</name>Val2</li>
                    <li name="name3"><value>c</value>Val3</li>
                    <li><name>name4</name><value>d</value>Val4</li>
                    <li>Val5</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]

        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(len(template_node.children), 5)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name1")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val1")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name2")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val2")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name3")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val3")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertEqual(node.name.children[0].word, "name4")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val4")

        node = template_node.children[4]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DEFAULT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val5")

    def test_condition_template_multi_typename_name_value_mixed_loop(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <li name='name1' value="a">Val1 <loop /></li>
                    <li value="b"><name>name2</name>Val2</li>
                    <li name="name3"><value>c</value>Val3</li>
                    <li><name>name4</name><value>d</value>Val4</li>
                    <li>Val5</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]

        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(len(template_node.children), 5)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertTrue(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name1")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val1")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name2")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val2")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name3")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val3")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(node.loop)
        self.assertEqual(node.name.children[0].word, "name4")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val4")

        node = template_node.children[4]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DEFAULT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val5")

    def test_condition_template_multi_typedata_name_value_mixed(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <li data='name1' value="a">Val1</li>
                    <li value="b"><data>name2</data>Val2</li>
                    <li data="name3"><value>c</value>Val3</li>
                    <li><data>name4</data><value>d</value>Val4</li>
                    <li>Val5</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]

        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(len(template_node.children), 5)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DATA)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name1")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val1")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DATA)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name2")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val2")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DATA)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name3")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val3")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DATA)
        self.assertFalse(node.loop)
        self.assertEqual(node.name.children[0].word, "name4")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val4")

        node = template_node.children[4]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DEFAULT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val5")

    def test_condition_template_multi_typedata_name_value_mixed_loop(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <li data='name1' value="a">Val1 <loop /></li>
                    <li value="b"><data>name2</data>Val2</li>
                    <li data="name3"><value>c</value>Val3</li>
                    <li><data>name4</data><value>d</value>Val4</li>
                    <li>Val5</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]

        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(len(template_node.children), 5)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DATA)
        self.assertTrue(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name1")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val1")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DATA)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name2")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val2")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DATA)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name3")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val3")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DATA)
        self.assertFalse(node.loop)
        self.assertEqual(node.name.children[0].word, "name4")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val4")

        node = template_node.children[4]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DEFAULT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val5")

    def test_condition_template_multi_typevar_name_value_mixed(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <li var='name1' value="a">Val1</li>
                    <li value="b"><var>name2</var>Val2</li>
                    <li var="name3"><value>c</value>Val3</li>
                    <li><var>name4</var><value>d</value>Val4</li>
                    <li>Val5</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]

        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(len(template_node.children), 5)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name1")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val1")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name2")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val2")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name3")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val3")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertEqual(node.name.children[0].word, "name4")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val4")

        node = template_node.children[4]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DEFAULT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val5")

    def test_condition_template_multi_typevar_name_value_mixed_loop(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <li var='name1' value="a">Val1 <loop /></li>
                    <li value="b"><var>name2</var>Val2</li>
                    <li var="name3"><value>c</value>Val3</li>
                    <li><var>name4</var><value>d</value>Val4</li>
                    <li>Val5</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]

        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(len(template_node.children), 5)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertTrue(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name1")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val1")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name2")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val2")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name3")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val3")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertEqual(node.name.children[0].word, "name4")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val4")

        node = template_node.children[4]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DEFAULT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val5")

    def test_condition_template_multi_bot_name_value_mixed(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <li bot='name1' value="a">Val1</li>
                    <li value="b"><bot>name2</bot>Val2</li>
                    <li bot="name3"><value>c</value>Val3</li>
                    <li><bot>name4</bot><value>d</value>Val4</li>
                    <li>Val5</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]

        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(len(template_node.children), 5)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name1")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val1")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name2")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val2")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name3")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val3")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertEqual(node.name.children[0].word, "name4")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val4")

        node = template_node.children[4]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DEFAULT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val5")

    def test_condition_template_multi_bot_name_value_mixed_loop(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <li bot='name1' value="a">Val1 <loop /></li>
                    <li value="b"><bot>name2</bot>Val2</li>
                    <li bot="name3"><value>c</value>Val3</li>
                    <li><bot>name4</bot><value>d</value>Val4</li>
                    <li>Val5</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]

        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(len(template_node.children), 5)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertTrue(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name1")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val1")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name2")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val2")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name3")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val3")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertEqual(node.name.children[0].word, "name4")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val4")

        node = template_node.children[4]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DEFAULT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val5")

    def test_condition_template_multi_type(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <li name='name1' value="a">Val1 <loop /></li>
                    <li value="b"><data>name2</data>Val2</li>
                    <li var="name3"><value>c</value>Val3</li>
                    <li><bot>name4</bot><value>d</value>Val4</li>
                    <li>Val5</li>
                </condition>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]

        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateConditionNode)
        self.assertEqual(len(template_node.children), 5)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.GLOBAL)
        self.assertTrue(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name1")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val1")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DATA)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name2")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val2")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name.children[0].word, "name3")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val3")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(node.loop)
        self.assertEqual(node.name.children[0].word, "name4")
        self.assertIsNotNone(node.value)
        self.assertIsInstance(node.value, TemplateNode)
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val4")

        node = template_node.children[4]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertEqual(node.var_type, TemplateConditionVariable.DEFAULT)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(self._client_context), "Val5")

    def test_condition_template_Multi_type_duplicate(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <li name='name1' value="a" var="name">Val1 <loop /></li>
                    <li value="b"><bot>name2</bot>Val2</li>
                    <li bot="name3"><value>c</value>Val3</li>
                    <li><bot>name4</bot><value>d</value>Val4</li>
                    <li>Val5</li>
                </condition>
            </template>
             """)
        with self.assertRaises(Exception):
            self._graph.parse_template_expression(template)

    def test_condition_template_invalid_tag(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <li name="name" value="a">Val1 <loop /></li>
                    <li value="b"><bot>name2</bot>Val2</li>
                    <li bot="name3"><value>c</value>Val3</li>
                    <li><bot>name4</bot><value>d</value>Val4</li>
                    <lx>Val5</lx>
                </condition>
            </template>
             """)
        with self.assertRaises(Exception):
            self._graph.parse_template_expression(template)

    def test_condition_template_default_with_value(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <li name="name" value="a">Val1 <loop /></li>
                    <li value="a">Val5</li>
                </condition>
            </template>
             """)
        with self.assertRaises(Exception):
            self._graph.parse_template_expression(template)

    def test_condition_template_not_default_no_value(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <li name="name">Val1 <loop /></li>
                    <li>Val5</li>
                </condition>
            </template>
             """)
        with self.assertRaises(Exception):
            self._graph.parse_template_expression(template)
