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

from programy.parser.exceptions import LimitOverException
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.condition import TemplateConditionValueNode
from programy.parser.template.nodes.condition import TemplateConditionVariable
from programy.parser.template.nodes.condition import TemplateConditionNode
from programy.parser.template.nodes.condition import TemplateConditionListItemNode
from programy.dialog.question import Question

from programytest.parser.base import ParserTestsBaseClass


class TemplateConditionVariableTests(ParserTestsBaseClass):

    def test_init_defaults(self):
        var = TemplateConditionVariable()
        self.assertIsNotNone(var)
        self.assertIsNone(var.name)
        self.assertIsNone(var.value)
        self.assertEqual(var.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(var.loop)

    def test_init_typename_as_default(self):
        name_node = TemplateConditionValueNode('name', 'var1')
        name_node.append(TemplateWordNode("var1"))
        value_node = TemplateConditionValueNode('value', 'value1')
        value_node.append(TemplateWordNode("value1"))
        var = TemplateConditionVariable(name=name_node, value=value_node)
        self.assertIsNotNone(var)
        self.assertEqual(var.name.to_string(), "var1")
        self.assertEqual(var.value.to_string(), "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(var.loop)

    def test_init_typename(self):
        name_node = TemplateConditionValueNode('name', 'var1')
        name_node.append(TemplateWordNode("var1"))
        value_node = TemplateConditionValueNode('value', 'value1')
        value_node.append(TemplateWordNode("value1"))
        var = TemplateConditionVariable(name=name_node, value=value_node, var_type=TemplateConditionVariable.GLOBAL)
        self.assertIsNotNone(var)
        self.assertEqual(var.name.to_string(), "var1")
        self.assertEqual(var.value.to_string(), "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(var.loop)

    def test_init_typename_with_loop(self):
        name_node = TemplateConditionValueNode('name', 'var1')
        name_node.append(TemplateWordNode("var1"))
        value_node = TemplateConditionValueNode('value', 'value1')
        value_node.append(TemplateWordNode("value1"))
        var = TemplateConditionVariable(name=name_node, value=value_node, var_type=TemplateConditionVariable.GLOBAL, loop=True)
        self.assertIsNotNone(var)
        self.assertEqual(var.name.to_string(), "var1")
        self.assertEqual(var.value.to_string(), "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.GLOBAL)
        self.assertTrue(var.loop)

    def test_init_typedata(self):
        name_node = TemplateConditionValueNode('data', 'var1')
        name_node.append(TemplateWordNode("var1"))
        value_node = TemplateConditionValueNode('value', 'value1')
        value_node.append(TemplateWordNode("value1"))
        var = TemplateConditionVariable(name=name_node, value=value_node, var_type=TemplateConditionVariable.DATA)
        self.assertIsNotNone(var)
        self.assertEqual(var.name.to_string(), "var1")
        self.assertEqual(var.value.to_string(), "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.DATA)
        self.assertFalse(var.loop)

    def test_init_typedata_with_loop(self):
        name_node = TemplateConditionValueNode('data', 'var1')
        name_node.append(TemplateWordNode("var1"))
        value_node = TemplateConditionValueNode('value', 'value1')
        value_node.append(TemplateWordNode("value1"))
        var = TemplateConditionVariable(name=name_node, value=value_node, var_type=TemplateConditionVariable.DATA, loop=True)
        self.assertIsNotNone(var)
        self.assertEqual(var.name.to_string(), "var1")
        self.assertEqual(var.value.to_string(), "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.DATA)
        self.assertTrue(var.loop)

    def test_init_typevar(self):
        name_node = TemplateConditionValueNode('var', 'var1')
        name_node.append(TemplateWordNode("var1"))
        value_node = TemplateConditionValueNode('value', 'value1')
        value_node.append(TemplateWordNode("value1"))
        var = TemplateConditionVariable(name=name_node, value=value_node,  var_type=TemplateConditionVariable.LOCAL)
        self.assertIsNotNone(var)
        self.assertEqual(var.name.to_string(), "var1")
        self.assertEqual(var.value.to_string(), "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(var.loop)

    def test_init_typevar_with_loop(self):
        name_node = TemplateConditionValueNode('var', 'var1')
        name_node.append(TemplateWordNode("var1"))
        value_node = TemplateConditionValueNode('value', 'value1')
        value_node.append(TemplateWordNode("value1"))
        var = TemplateConditionVariable(name=name_node, value=value_node, var_type=TemplateConditionVariable.LOCAL, loop=True)
        self.assertIsNotNone(var)
        self.assertEqual(var.name.to_string(), "var1")
        self.assertEqual(var.value.to_string(), "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.LOCAL)
        self.assertTrue(var.loop)

    def test_init_bot(self):
        name_node = TemplateConditionValueNode('bot', 'var1')
        name_node.append(TemplateWordNode("var1"))
        value_node = TemplateConditionValueNode('value', 'value1')
        value_node.append(TemplateWordNode("value1"))
        var = TemplateConditionVariable(name=name_node, value=value_node, var_type=TemplateConditionVariable.BOT)
        self.assertIsNotNone(var)
        self.assertEqual(var.name.to_string(), "var1")
        self.assertEqual(var.value.to_string(), "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(var.loop)

    def test_init_bot_with_loop(self):
        name_node = TemplateConditionValueNode('bot', 'var1')
        name_node.append(TemplateWordNode("var1"))
        value_node = TemplateConditionValueNode('value', 'value1')
        value_node.append(TemplateWordNode("value1"))
        var = TemplateConditionVariable(name=name_node, value=value_node, var_type=TemplateConditionVariable.BOT, loop=True)
        self.assertIsNotNone(var)
        self.assertEqual(var.name.to_string(), "var1")
        self.assertEqual(var.value.to_string(), "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.BOT)
        self.assertTrue(var.loop)


class TemplateConditionListItemNodeTests(ParserTestsBaseClass):

    def test_init_defaults(self):
        var = TemplateConditionListItemNode()
        self.assertIsNotNone(var)
        self.assertIsNone(var.name)
        self.assertIsNone(var.value)
        self.assertEqual(var.var_type, TemplateConditionListItemNode.GLOBAL)
        self.assertFalse(var.loop)
        self.assertTrue(var.is_default())
        self.assertEqual("[CONDITIONLIST]", var.to_string())
        self.assertEqual("<li></li>", var.to_xml(self._client_context))

    def test_init_typename_as_default(self):
        name_node = TemplateConditionValueNode('name', 'var1')
        name_node.append(TemplateWordNode("var1"))
        value_node = TemplateConditionValueNode('value', 'value1')
        value_node.append(TemplateWordNode("value1"))
        var = TemplateConditionListItemNode(name=name_node, value=value_node)
        self.assertIsNotNone(var)
        self.assertEqual(var.name.to_string(), "var1")
        self.assertEqual(var.value.to_string(), "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.GLOBAL)
        self.assertFalse(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual('[CONDITIONLIST(name="var1" value="value1")]', var.to_string())
        self.assertEqual('<li><name>var1</name><value>value1</value></li>', var.to_xml(self._client_context))

    def test_init_typename(self):
        name_node = TemplateConditionValueNode('name', 'var1')
        name_node.append(TemplateWordNode("var1"))
        value_node = TemplateConditionValueNode('value', 'value1')
        value_node.append(TemplateWordNode("value1"))
        var = TemplateConditionListItemNode(name=name_node, value=value_node, var_type=TemplateConditionListItemNode.GLOBAL)
        self.assertIsNotNone(var)
        self.assertEqual(var.name.to_string(), "var1")
        self.assertEqual(var.value.to_string(), "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.GLOBAL)
        self.assertFalse(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual('[CONDITIONLIST(name="var1" value="value1")]', var.to_string())
        self.assertEqual('<li><name>var1</name><value>value1</value></li>', var.to_xml(self._client_context))

    def test_init_typename_with_loop(self):
        name_node = TemplateConditionValueNode('name', 'var1')
        name_node.append(TemplateWordNode("var1"))
        value_node = TemplateConditionValueNode('value', 'value1')
        value_node.append(TemplateWordNode("value1"))
        var = TemplateConditionListItemNode(name=name_node, value=value_node, var_type=TemplateConditionListItemNode.GLOBAL, loop=True)
        self.assertIsNotNone(var)
        self.assertEqual(var.name.to_string(), "var1")
        self.assertEqual(var.value.to_string(), "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.GLOBAL)
        self.assertTrue(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual('[CONDITIONLIST(name="var1" value="value1")]', var.to_string())
        self.assertEqual('<li><name>var1</name><value>value1</value><loop /></li>', var.to_xml(self._client_context))

    def test_init_typedata(self):
        name_node = TemplateConditionValueNode('data', 'var1')
        name_node.append(TemplateWordNode("var1"))
        value_node = TemplateConditionValueNode('value', 'value1')
        value_node.append(TemplateWordNode("value1"))
        var = TemplateConditionListItemNode(name=name_node, value=value_node, var_type=TemplateConditionListItemNode.DATA)
        self.assertIsNotNone(var)
        self.assertEqual(var.name.to_string(), "var1")
        self.assertEqual(var.value.to_string(), "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.DATA)
        self.assertFalse(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual('[CONDITIONLIST(data="var1" value="value1")]', var.to_string())
        self.assertEqual('<li><data>var1</data><value>value1</value></li>', var.to_xml(self._client_context))

    def test_init_typedata_with_loop(self):
        name_node = TemplateConditionValueNode('data', 'var1')
        name_node.append(TemplateWordNode("var1"))
        value_node = TemplateConditionValueNode('value', 'value1')
        value_node.append(TemplateWordNode("value1"))
        var = TemplateConditionListItemNode(name=name_node, value=value_node, var_type=TemplateConditionListItemNode.DATA, loop=True)
        self.assertIsNotNone(var)
        self.assertEqual(var.name.to_string(), "var1")
        self.assertEqual(var.value.to_string(), "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.DATA)
        self.assertTrue(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual('[CONDITIONLIST(data="var1" value="value1")]', var.to_string())
        self.assertEqual('<li><data>var1</data><value>value1</value><loop /></li>', var.to_xml(self._client_context))

    def test_init_typevar(self):
        name_node = TemplateConditionValueNode('var', 'var1')
        name_node.append(TemplateWordNode("var1"))
        value_node = TemplateConditionValueNode('value', 'value1')
        value_node.append(TemplateWordNode("value1"))
        var = TemplateConditionListItemNode(name=name_node, value=value_node, var_type=TemplateConditionListItemNode.LOCAL)
        self.assertIsNotNone(var)
        self.assertEqual(var.name.to_string(), "var1")
        self.assertEqual(var.value.to_string(), "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.LOCAL)
        self.assertFalse(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual('[CONDITIONLIST(var="var1" value="value1")]', var.to_string())
        self.assertEqual('<li><var>var1</var><value>value1</value></li>', var.to_xml(self._client_context))

    def test_init_typevar_with_loop(self):
        name_node = TemplateConditionValueNode('var', 'var1')
        name_node.append(TemplateWordNode("var1"))
        value_node = TemplateConditionValueNode('value', 'value1')
        value_node.append(TemplateWordNode("value1"))
        var = TemplateConditionListItemNode(name=name_node, value=value_node, var_type=TemplateConditionListItemNode.LOCAL, loop=True)
        self.assertIsNotNone(var)
        self.assertEqual(var.name.to_string(), "var1")
        self.assertEqual(var.value.to_string(), "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.LOCAL)
        self.assertTrue(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual('[CONDITIONLIST(var="var1" value="value1")]', var.to_string())
        self.assertEqual('<li><var>var1</var><value>value1</value><loop /></li>', var.to_xml(self._client_context))

    def test_init_bot(self):
        name_node = TemplateConditionValueNode('bot', 'var1')
        name_node.append(TemplateWordNode("var1"))
        value_node = TemplateConditionValueNode('value', 'value1')
        value_node.append(TemplateWordNode("value1"))
        var = TemplateConditionListItemNode(name=name_node, value=value_node, var_type=TemplateConditionListItemNode.BOT)
        self.assertIsNotNone(var)
        self.assertEqual(var.name.to_string(), "var1")
        self.assertEqual(var.value.to_string(), "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.BOT)
        self.assertFalse(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual('[CONDITIONLIST(bot="var1" value="value1")]', var.to_string())
        self.assertEqual('<li><bot>var1</bot><value>value1</value></li>', var.to_xml(self._client_context))

    def test_init_bot_with_loop(self):
        name_node = TemplateConditionValueNode('bot', 'var1')
        name_node.append(TemplateWordNode("var1"))
        value_node = TemplateConditionValueNode('value', 'value1')
        value_node.append(TemplateWordNode("value1"))
        var = TemplateConditionListItemNode(name=name_node, value=value_node, var_type=TemplateConditionListItemNode.BOT, loop=True)
        self.assertIsNotNone(var)
        self.assertEqual(var.name.to_string(), "var1")
        self.assertEqual(var.value.to_string(), "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.BOT)
        self.assertTrue(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual('[CONDITIONLIST(bot="var1" value="value1")]', var.to_string())
        self.assertEqual('<li><bot>var1</bot><value>value1</value><loop /></li>', var.to_xml(self._client_context))


class TemplateConditionNodeTests(ParserTestsBaseClass):

    ###################################################################################################################
    # Type 1 Name
    #

    def test_type1_node_typename_match(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        name_node = TemplateConditionValueNode('name')
        name_node.append(TemplateWordNode("name1"))
        value_node = TemplateConditionValueNode('value')
        value_node.append(TemplateWordNode("value1"))
        node = TemplateConditionNode(name_node, value_node, var_type=TemplateConditionNode.GLOBAL)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.bot.get_conversation(self._client_context).set_property('name1', "value1")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual(result, "Hello")

    def test_type1_node_typename_nomatch(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        name_node = TemplateConditionValueNode('name')
        name_node.append(TemplateWordNode("name1"))
        value_node = TemplateConditionValueNode('value')
        value_node.append(TemplateWordNode("value1"))
        node = TemplateConditionNode(name_node, value_node, var_type=TemplateConditionNode.GLOBAL)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.bot.get_conversation(self._client_context).set_property('name1', "value2")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual(result, "")

    def test_type1_to_xml_typename(self):
        root = TemplateNode()
        name_node = TemplateConditionValueNode('name')
        name_node.append(TemplateWordNode("name1"))
        value_node = TemplateConditionValueNode('value')
        value_node.append(TemplateWordNode("value1"))
        node = TemplateConditionNode(name_node, value_node, var_type=TemplateConditionNode.GLOBAL)
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition><name>name1</name><value>value1</value>Hello</condition></template>', xml_str)

    ###################################################################################################################
    # Type 1 Data
    #

    def test_type1_node_typedata_match(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        name_node = TemplateConditionValueNode('data')
        name_node.append(TemplateWordNode("name1"))
        value_node = TemplateConditionValueNode('value')
        value_node.append(TemplateWordNode("value1"))
        node = TemplateConditionNode(name_node, value_node, var_type=TemplateConditionNode.DATA)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.bot.get_conversation(self._client_context).set_data_property('name1', "value1")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual(result, "Hello")

    def test_type1_node_typedata_nomatch(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        name_node = TemplateConditionValueNode('data')
        name_node.append(TemplateWordNode("name1"))
        value_node = TemplateConditionValueNode('value')
        value_node.append(TemplateWordNode("value1"))
        node = TemplateConditionNode(name_node, value_node, var_type=TemplateConditionNode.DATA)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.bot.get_conversation(self._client_context).set_data_property('name1', "value2")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual(result, "")

    def test_type1_to_xml_typedata(self):
        root = TemplateNode()
        name_node = TemplateConditionValueNode('data')
        name_node.append(TemplateWordNode("name1"))
        value_node = TemplateConditionValueNode('value')
        value_node.append(TemplateWordNode("value1"))
        node = TemplateConditionNode(name_node, value_node, var_type=TemplateConditionNode.DATA)
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition><data>name1</data><value>value1</value>Hello</condition></template>', xml_str)

    ###################################################################################################################
    # Type 1 var
    #

    def test_type1_node_typevar_match(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        name_node = TemplateConditionValueNode('var')
        name_node.append(TemplateWordNode("var1"))
        value_node = TemplateConditionValueNode('value')
        value_node.append(TemplateWordNode("value1"))
        node = TemplateConditionNode(name_node, value_node, var_type=TemplateConditionNode.LOCAL)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        question = Question.create_from_text(self._client_context, "Hello")
        self._client_context.bot.get_conversation(self._client_context).record_dialog(question)
        self._client_context.bot.get_conversation(self._client_context).current_question().set_property("var1", "value1")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual(result, "Hello")

    def test_type1_node_typevar_nomatch(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        name_node = TemplateConditionValueNode('var')
        name_node.append(TemplateWordNode("name1"))
        value_node = TemplateConditionValueNode('value')
        value_node.append(TemplateWordNode("value1"))
        node = TemplateConditionNode(name_node, value_node, var_type=TemplateConditionNode.LOCAL)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        question = Question.create_from_text(self._client_context, "Hello")
        self._client_context.bot.get_conversation(self._client_context).record_dialog(question)
        self._client_context.bot.get_conversation(self._client_context).current_question().set_property("var1", "value2")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual(result, "")

    def test_type1_to_xml_typevar(self):
        root = TemplateNode()
        name_node = TemplateConditionValueNode('var')
        name_node.append(TemplateWordNode("name1"))
        value_node = TemplateConditionValueNode('value')
        value_node.append(TemplateWordNode("value1"))
        node = TemplateConditionNode(name_node, value_node, var_type=TemplateConditionNode.LOCAL)
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition><var>name1</var><value>value1</value>Hello</condition></template>', xml_str)

    ###################################################################################################################
    # Type 1 Bot
    #

    def test_type1_node_bot_match(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        name_node = TemplateConditionValueNode('bot')
        name_node.append(TemplateWordNode("name1"))
        value_node = TemplateConditionValueNode('value')
        value_node.append(TemplateWordNode("value1"))
        node = TemplateConditionNode(name_node, value_node, var_type=TemplateConditionNode.BOT)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property('name1', "value1")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual(result, "Hello")

    def test_type1_node_bot_nomatch(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        name_node = TemplateConditionValueNode('bot')
        name_node.append(TemplateWordNode("name1"))
        value_node = TemplateConditionValueNode('value')
        value_node.append(TemplateWordNode("value1"))
        node = TemplateConditionNode(name_node, value_node, var_type=TemplateConditionNode.BOT)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property('name1', "value2")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual(result, "")

    def test_type1_to_xml_bot(self):
        root = TemplateNode()
        name_node = TemplateConditionValueNode('bot')
        name_node.append(TemplateWordNode("name1"))
        value_node = TemplateConditionValueNode('value')
        value_node.append(TemplateWordNode("value1"))
        node = TemplateConditionNode(name_node, value_node, var_type=TemplateConditionNode.BOT)
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition><bot>name1</bot><value>value1</value>Hello</condition></template>', xml_str)

    ###################################################################################################################
    # Type 2 Name
    #

    def test_type2_node_typename(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        name_node = TemplateConditionValueNode('name')
        name_node.append(TemplateWordNode("cond1"))
        node = TemplateConditionNode(name_node, condition_type=2)
        self.assertIsNotNone(node)
        value_node1 = TemplateConditionValueNode('value')
        value_node1.append(TemplateWordNode("value1"))
        cond1 = TemplateConditionListItemNode(value=value_node1)
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        value_node2 = TemplateConditionValueNode('value')
        value_node2.append(TemplateWordNode("value2"))
        cond2 = TemplateConditionListItemNode(value=value_node2)
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.bot.get_conversation(self._client_context).set_property('cond1', "value2")

        question = Question.create_from_text(self._client_context, "Hello")
        self._client_context.bot.get_conversation(self._client_context).record_dialog(question)
        self._client_context.bot.get_conversation(self._client_context).current_question().set_property("cond1", "value2")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("Word2", result)

    def test_type2_node_loop(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        name_node = TemplateConditionValueNode('name')
        name_node.append(TemplateWordNode("cond1"))
        node = TemplateConditionNode(name_node, condition_type=2)
        self.assertIsNotNone(node)
        value_node = TemplateConditionValueNode('value')
        value_node.append(TemplateWordNode("value1"))
        cond1 = TemplateConditionListItemNode(value=value_node, loop=True)
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.bot.configuration._max_search_condition = 5
        self._client_context.bot.get_conversation(self._client_context).set_property('cond1', "value1")

        with self.assertRaises(LimitOverException):
            root.resolve(self._client_context)

    def test_type2_to_xml_typename(self):
        root = TemplateNode()

        name_node = TemplateConditionValueNode('name')
        name_node.append(TemplateWordNode("cond1"))
        node = TemplateConditionNode(name_node, condition_type=2)
        self.assertIsNotNone(node)
        value_node1 = TemplateConditionValueNode('value')
        value_node1.append(TemplateWordNode("value1"))
        cond1 = TemplateConditionListItemNode(value=value_node1)
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        value_node2 = TemplateConditionValueNode('value')
        value_node2.append(TemplateWordNode("value2"))
        cond2 = TemplateConditionListItemNode(value=value_node2)
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition><name>cond1</name><li><value>value1</value>Word1</li><li><value>value2</value>Word2</li>'
                         '<li>Word3</li></condition></template>', xml_str)

    ###################################################################################################################
    # Type 2 Data
    #

    def test_type2_node_typedata(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        name_node = TemplateConditionValueNode('data')
        name_node.append(TemplateWordNode("cond1"))
        node = TemplateConditionNode(name_node, var_type=TemplateConditionNode.DATA, condition_type=2)
        self.assertIsNotNone(node)
        value_node1 = TemplateConditionValueNode('value')
        value_node1.append(TemplateWordNode("value1"))
        cond1 = TemplateConditionListItemNode(value=value_node1)
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        value_node2 = TemplateConditionValueNode('value')
        value_node2.append(TemplateWordNode("value2"))
        cond2 = TemplateConditionListItemNode(value=value_node2)
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.bot.get_conversation(self._client_context).set_data_property('cond1', "value2")

        question = Question.create_from_text(self._client_context, "Hello")
        self._client_context.bot.get_conversation(self._client_context).record_dialog(question)
        self._client_context.bot.get_conversation(self._client_context).current_question().set_property("cond1", "value2")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("Word2", result)

    def test_type2_to_xml_typedata(self):
        root = TemplateNode()

        name_node = TemplateConditionValueNode('data')
        name_node.append(TemplateWordNode("cond1"))
        node = TemplateConditionNode(name_node, var_type=TemplateConditionNode.DATA, condition_type=2)
        self.assertIsNotNone(node)
        value_node1 = TemplateConditionValueNode('value')
        value_node1.append(TemplateWordNode("value1"))
        cond1 = TemplateConditionListItemNode(value=value_node1)
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        value_node2 = TemplateConditionValueNode('value')
        value_node2.append(TemplateWordNode("value2"))
        cond2 = TemplateConditionListItemNode(value=value_node2)
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition><data>cond1</data><li><value>value1</value>Word1</li>'
                         '<li><value>value2</value>Word2</li><li>Word3</li></condition></template>', xml_str)

    ###################################################################################################################
    # Type 2 Var
    #

    def test_type2_node_typevar(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        name_node = TemplateConditionValueNode('var')
        name_node.append(TemplateWordNode("var1"))
        node = TemplateConditionNode(name_node, var_type=TemplateConditionNode.LOCAL, condition_type=2)
        self.assertIsNotNone(node)
        value_node1 = TemplateConditionValueNode('value')
        value_node1.append(TemplateWordNode("value1"))
        cond1 = TemplateConditionListItemNode(value=value_node1, var_type=TemplateConditionNode.LOCAL)
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        value_node2 = TemplateConditionValueNode('value')
        value_node2.append(TemplateWordNode("value2"))
        cond2 = TemplateConditionListItemNode(value=value_node2, var_type=TemplateConditionNode.LOCAL)
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        question = Question.create_from_text(self._client_context, "Hello")
        self._client_context.bot.get_conversation(self._client_context).record_dialog(question)
        self._client_context.bot.get_conversation(self._client_context).current_question().set_property("var1", "value2")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("Word2", result)

    def test_type2_to_xml_typevar(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        name_node = TemplateConditionValueNode('var')
        name_node.append(TemplateWordNode("var1"))
        node = TemplateConditionNode(name_node, var_type=TemplateConditionNode.LOCAL, condition_type=2)
        self.assertIsNotNone(node)
        value_node1 = TemplateConditionValueNode('value')
        value_node1.append(TemplateWordNode("value1"))
        cond1 = TemplateConditionListItemNode(value=value_node1, var_type=TemplateConditionNode.LOCAL)
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        value_node2 = TemplateConditionValueNode('value')
        value_node2.append(TemplateWordNode("value2"))
        cond2 = TemplateConditionListItemNode(value=value_node2, var_type=TemplateConditionNode.LOCAL)
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition><var>var1</var><li><value>value1</value>Word1</li><li><value>value2</value>Word2</li><li>Word3</li></condition></template>', xml_str)

    ###################################################################################################################
    # Type 2 Bot
    #

    def test_type2_node_bot(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        name_node = TemplateConditionValueNode('bot')
        name_node.append(TemplateWordNode("cond1"))
        node = TemplateConditionNode(name_node, var_type=TemplateConditionNode.BOT, condition_type=2)
        self.assertIsNotNone(node)
        value_node1 = TemplateConditionValueNode('value')
        value_node1.append(TemplateWordNode("value1"))
        cond1 = TemplateConditionListItemNode(value=value_node1, var_type=TemplateConditionNode.BOT)
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        value_node2 = TemplateConditionValueNode('value')
        value_node2.append(TemplateWordNode("value2"))
        cond2 = TemplateConditionListItemNode(value=value_node2, var_type=TemplateConditionNode.BOT)
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property('cond1', "value2")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("Word2", result)

    def test_type2_to_xml_bot(self):
        root = TemplateNode()

        name_node = TemplateConditionValueNode('bot')
        name_node.append(TemplateWordNode("cond1"))
        node = TemplateConditionNode(name_node, var_type=TemplateConditionNode.BOT, condition_type=2)
        self.assertIsNotNone(node)
        value_node1 = TemplateConditionValueNode('value')
        value_node1.append(TemplateWordNode("value1"))
        cond1 = TemplateConditionListItemNode(value=value_node1)
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        value_node2 = TemplateConditionValueNode('value')
        value_node2.append(TemplateWordNode("value2"))
        cond2 = TemplateConditionListItemNode(value=value_node2)
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition><bot>cond1</bot><li><value>value1</value>Word1</li>'
                         '<li><value>value2</value>Word2</li><li>Word3</li></condition></template>', xml_str)

    ###################################################################################################################
    # Type 3

    def test_type3_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode(condition_type=3)
        self.assertIsNotNone(node)

        name_node1 = TemplateConditionValueNode('name')
        name_node1.append(TemplateWordNode("name1"))
        value_node1 = TemplateConditionValueNode('value')
        value_node1.append(TemplateWordNode("value1"))
        cond1 = TemplateConditionListItemNode(name=name_node1, value=value_node1, var_type=TemplateConditionNode.GLOBAL)
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)

        name_node2 = TemplateConditionValueNode('data')
        name_node2.append(TemplateWordNode("name2"))
        value_node2 = TemplateConditionValueNode('value')
        value_node2.append(TemplateWordNode("value2"))
        cond2 = TemplateConditionListItemNode(name=name_node2, value=value_node2, var_type=TemplateConditionNode.DATA)
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)

        name_node3 = TemplateConditionValueNode('var')
        name_node3.append(TemplateWordNode("name3"))
        value_node3 = TemplateConditionValueNode('value')
        value_node3.append(TemplateWordNode("value3"))
        cond3 = TemplateConditionListItemNode(name=name_node3, value=value_node3, var_type=TemplateConditionNode.LOCAL)
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        name_node4 = TemplateConditionValueNode('bot')
        name_node4.append(TemplateWordNode("name4"))
        value_node4 = TemplateConditionValueNode('value')
        value_node4.append(TemplateWordNode("value4"))
        cond4 = TemplateConditionListItemNode(name=name_node4, value=value_node4, var_type=TemplateConditionNode.BOT)
        cond4.append(TemplateWordNode("Word4"))
        node.append(cond4)

        cond5 = TemplateConditionListItemNode()
        cond5.append(TemplateWordNode("Word5"))
        node.append(cond5)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.bot.get_conversation(self._client_context).set_property('name1', "value1")
        self._client_context.brain.properties.add_property('name4', "value4")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("Word1", result)

        self._client_context.bot.get_conversation(self._client_context).set_property('name1', "value2")

        self._client_context.brain.properties.add_property('name4', "value4")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("Word4", result)

    def test_type3_node_loop(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode(condition_type=3)
        self.assertIsNotNone(node)

        name_node = TemplateConditionValueNode('name')
        name_node.append(TemplateWordNode("name1"))
        value_node = TemplateConditionValueNode('value')
        value_node.append(TemplateWordNode("value1"))
        cond1 = TemplateConditionListItemNode(name=name_node, value=value_node, var_type=TemplateConditionNode.GLOBAL, loop=True)
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.bot.configuration._max_search_condition = 5
        self._client_context.bot.get_conversation(self._client_context).set_property('name1', "value1")

        with self.assertRaises(LimitOverException):
            root.resolve(self._client_context)

    def test_type3_to_xml(self):
        root = TemplateNode()

        node = TemplateConditionNode(condition_type=3)
        self.assertIsNotNone(node)

        name_node1 = TemplateConditionValueNode('name')
        name_node1.append(TemplateWordNode("name1"))
        value_node1 = TemplateConditionValueNode('value')
        value_node1.append(TemplateWordNode("value1"))
        cond1 = TemplateConditionListItemNode(name=name_node1, value=value_node1, var_type=TemplateConditionNode.GLOBAL)
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)

        name_node2 = TemplateConditionValueNode('data')
        name_node2.append(TemplateWordNode("name2"))
        value_node2 = TemplateConditionValueNode('value')
        value_node2.append(TemplateWordNode("value2"))
        cond2 = TemplateConditionListItemNode(name=name_node2, value=value_node2, var_type=TemplateConditionNode.DATA)
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)

        name_node3 = TemplateConditionValueNode('var')
        name_node3.append(TemplateWordNode("name3"))
        value_node3 = TemplateConditionValueNode('value')
        value_node3.append(TemplateWordNode("value3"))
        cond3 = TemplateConditionListItemNode(name=name_node3, value=value_node3, var_type=TemplateConditionNode.LOCAL)
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        name_node4 = TemplateConditionValueNode('bot')
        name_node4.append(TemplateWordNode("name4"))
        value_node4 = TemplateConditionValueNode('value')
        value_node4.append(TemplateWordNode("value4"))
        cond4 = TemplateConditionListItemNode(name=name_node4, value=value_node4, var_type=TemplateConditionNode.BOT)
        cond4.append(TemplateWordNode("Word4"))
        node.append(cond4)

        cond5 = TemplateConditionListItemNode()
        cond5.append(TemplateWordNode("Word5"))
        node.append(cond5)

        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        texts = '<template><condition><li><name>name1</name><value>value1</value>Word1</li><li><data>name2</data><value>value2</value>Word2</li>' + \
            '<li><var>name3</var><value>value3</value>Word3</li>' + \
            '<li><bot>name4</bot><value>value4</value>Word4</li><li>Word5</li></condition></template>'
        self.assertEqual(texts, xml_str)
